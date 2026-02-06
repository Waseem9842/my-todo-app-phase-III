// Service for handling Better Auth integration
import { User } from '../types/chat';

/**
 * Service class for handling authentication with Better Auth
 */
export class AuthService {
  /**
   * Gets the current user's JWT token from storage
   * @returns The JWT token string or null if not authenticated
   */
  static getToken(): string | null {
    if (typeof window !== 'undefined') {
      // Get token from our custom JWT storage (matches AuthProvider)
      return localStorage.getItem('jwt_token') ||
             sessionStorage.getItem('jwt_token') ||
             null;
    }
    return null;
  }

  /**
   * Checks if the user is currently authenticated
   * @returns Boolean indicating authentication status
   */
  static isAuthenticated(): boolean {
    const token = this.getToken();
    if (!token) {
      return false;
    }

    // Decode token to check if it's expired
    try {
      const payload = this.parseJwtPayload(token);
      const currentTime = Math.floor(Date.now() / 1000);
      return payload.exp > currentTime;
    } catch (error) {
      console.error('Error validating token:', error);
      return false;
    }
  }

  /**
   * Parses the payload from a JWT token
   * @param token The JWT token string
   * @returns The decoded payload object
   */
  private static parseJwtPayload(token: string): { [key: string]: any } {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );

    return JSON.parse(jsonPayload);
  }

  /**
   * Gets the user ID from the JWT token
   * @returns The user ID string or null if not available
   */
  static getUserId(): string | null {
    const token = this.getToken();
    if (!token) {
      return null;
    }

    try {
      const payload = this.parseJwtPayload(token);
      // Common JWT claims for user ID: sub, user_id, id
      return payload.sub || payload.user_id || payload.id || null;
    } catch (error) {
      console.error('Error extracting user ID from token:', error);
      return null;
    }
  }

  /**
   * Sets the authentication token in storage
   * @param token The JWT token to store
   * @param useSessionStorage Whether to use sessionStorage instead of localStorage
   */
  static setToken(token: string, useSessionStorage: boolean = false): void {
    if (typeof window !== 'undefined') {
      if (useSessionStorage) {
        localStorage.setItem('jwt_token', token);
      } else {
        localStorage.setItem('jwt_token', token);
      }
    }
  }

  /**
   * Clears the authentication token from storage
   */
  static clearToken(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('jwt_token');
      sessionStorage.removeItem('jwt_token');
    }
  }

  /**
   * Refreshes the authentication token if expired
   * @returns Promise resolving to success status
   */
  static async refreshToken(): Promise<boolean> {
    // In a real implementation, this would call the Better Auth refresh endpoint
    // For now, we'll return true to indicate that refresh is not needed
    // since Better Auth typically handles token refresh automatically
    console.warn('Token refresh not implemented - Better Auth should handle this automatically');
    return true;
  }

  /**
   * Validates that a user has access to a specific resource
   * @param userId The ID of the user requesting access
   * @param resourceId The ID of the resource being accessed
   * @param resourceOwnerUserId The ID of the user who owns the resource
   * @returns Boolean indicating if access is allowed
   */
  static validateUserResourceAccess(userId: string, resourceId: string, resourceOwnerUserId: string): boolean {
    // Ensure the requesting user is the same as the resource owner
    return userId === resourceOwnerUserId;
  }

  /**
   * Gets the current user information
   * @returns User object with user ID and token information
   */
  static getCurrentUser(): User | null {
    const userId = this.getUserId();
    const token = this.getToken();

    if (!userId) {
      return null;
    }

    return {
      user_id: userId,
      jwt_token: token || undefined
    };
  }
}