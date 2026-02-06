// API client utilities for the frontend
// Centralized API client for making authenticated requests to the backend

import { getToken } from './auth';

// Base API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

/**
 * Makes an authenticated API request
 * @param endpoint - The API endpoint to call
 * @param options - Request options including method, body, etc.
 * @returns Promise with the response data
 */
export async function authenticatedRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  // Prepare headers with JWT token if available
  const headers = new Headers(options.headers);

  // Add JWT token to authorization header if authenticated
  const token = getToken();
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  // Set default content type if not already set
  if (!headers.has('Content-Type') && options.body) {
    headers.set('Content-Type', 'application/json');
  }

  // Construct full URL
  const url = `${API_BASE_URL}${endpoint}`;
  let response;

  try {
    response = await fetch(url, {
      ...options,
      headers,
    });

    // If response is 401 (Unauthorized), consider token expired
    if (response.status === 401) {
      // In a real app, we'd want to remove the token and redirect to login
      // localStorage.removeItem('jwt_token');
      throw new Error('Unauthorized: Please sign in again');
    }

    // If response is 403 (Forbidden), handle accordingly
    if (response.status === 403) {
      throw new Error('Forbidden: Access denied');
    }

    // Try to parse response based on status and content type
    let data;

    // Handle different response statuses appropriately
    if (response.status === 204) {
      // For 204 No Content responses (like successful DELETE)
      return undefined as any;
    } else {
      const contentType = response.headers.get('content-type');

      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      } else {
        // For non-JSON responses
        data = await response.text();
      }
    }

    if (!response.ok) {
      // Handle error responses - data might be an object, array, or string
      let errorMessage = `HTTP error! status: ${response.status}`;

      if (Array.isArray(data)) {
        // Handle validation errors array like [{"type":"missing","loc":["query","completed"],"msg":"Field required","input":null}]
        const validationErrors = data.map(error => {
          if (typeof error === 'object' && error !== null && 'msg' in error) {
            return error.msg;
          }
          return JSON.stringify(error);
        }).join('; ');

        errorMessage = validationErrors;
      } else if (typeof data === 'object' && data !== null) {
        // If data is an object, try to extract the detail property
        if ('detail' in data) {
          // The detail might be a string or an object/array
          if (typeof data.detail === 'string') {
            errorMessage = data.detail;
          } else if (Array.isArray(data.detail)) {
            // If detail is an array (like validation errors), extract messages
            const detailErrors = data.detail.map((err: any) => {
              if (typeof err === 'object' && err !== null && 'msg' in err) {
                return err.msg;
              }
              return JSON.stringify(err);
            }).join('; ');

            errorMessage = detailErrors;
          } else if (typeof data.detail === 'object') {
            // If detail is an object, try to extract message if available
            if ('msg' in data.detail) {
              errorMessage = data.detail.msg;
            } else {
              errorMessage = JSON.stringify(data.detail);
            }
          } else {
            // For other types, convert to string
            errorMessage = String(data.detail);
          }
        } else {
          // If no detail property, try to stringify the entire object
          errorMessage = JSON.stringify(data);
        }
      } else if (typeof data === 'string' && data) {
        // If data is a string, use it as the error message
        errorMessage = data;
      } else if (response.statusText) {
        // If there's a status text, use that
        errorMessage = response.statusText;
      }

      throw new Error(errorMessage);
    }

    return data;
  } catch (error) {
    console.error(`API request error for ${url}:`, error);
    throw error;
  }
}

// Export individual methods for convenience
export const apiClient = {
  get: <T>(endpoint: string) => authenticatedRequest<T>(endpoint, { method: 'GET' }),
  post: <T>(endpoint: string, data?: any) => authenticatedRequest<T>(endpoint, {
    method: 'POST',
    body: data ? JSON.stringify(data) : undefined,
  }),
  put: <T>(endpoint: string, data: any) => authenticatedRequest<T>(endpoint, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  patch: <T>(endpoint: string, data: any) => authenticatedRequest<T>(endpoint, {
    method: 'PATCH',
    body: JSON.stringify(data),
  }),
  delete: <T>(endpoint: string) => authenticatedRequest<T>(endpoint, { method: 'DELETE' }),
};