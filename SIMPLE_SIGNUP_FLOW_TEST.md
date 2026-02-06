# Authentication Flow Test Instructions

## Test the Signup and Sign-In Process

### Backend Authentication Testing (Completed)
The backend authentication system has been verified to work correctly:

1. **Signup Test** (Already Verified):
   ```bash
   curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"johndoe@example.com", "password":"password123", "name":"John Doe"}'
   ```

2. **Signin Test** (Already Verified):
   ```bash
   curl -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"johndoe@example.com", "password":"password123"}'
   ```

3. **Protected Route Test** (Already Verified):
   ```bash
   # Using the token from login response
   curl -X GET http://localhost:8000/api/auth/me \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
   ```

### Frontend UI Testing Instructions

#### Step 1: Start the Applications
1. Ensure backend is running:
   ```bash
   cd /mnt/e/Hackathon2_todo_app/phase-III/backend
   python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. Start the frontend (in a separate terminal):
   ```bash
   cd /mnt/e/Hackathon2_todo_app/phase-III/frontend
   npm run dev
   ```

#### Step 2: Test Signup Process
1. Navigate to: `http://localhost:3000/signup`
2. Fill in the signup form:
   - Name: "Test User"
   - Email: "testuser@example.com"
   - Password: "password123"
3. Click "Sign Up"
4. Verify you're redirected to the dashboard

#### Step 3: Test Signin Process
1. Navigate to: `http://localhost:3000/signin`
2. Fill in the signin form:
   - Email: "testuser@example.com"
   - Password: "password123"
3. Click "Sign In"
4. Verify you're redirected to the dashboard

#### Step 4: Test Task Creation via Chatbot
1. After signing in, navigate to the chat interface
2. Try creating a task using natural language:
   - "Create a task to buy groceries"
   - "Add a task to call mom"
3. Verify the tasks are created successfully

### Expected Results
- Sign up form should register the user and redirect to dashboard
- Sign in form should authenticate the user and redirect to dashboard
- Chatbot should accept natural language commands and create tasks
- UI should render properly without hanging or blank screens

### Troubleshooting
If the frontend still doesn't render properly:
1. Check browser console for JavaScript errors
2. Verify NEXT_PUBLIC_API_BASE_URL is set to `http://localhost:8000`
3. Clear browser cache and localStorage
4. Check that the backend is accessible from the frontend

### Fixed Issues
- ✅ Consistent token storage across all components
- ✅ Proper authentication flow between frontend and backend
- ✅ Resolved conflicts between custom JWT auth and Better Auth references
- ✅ Standardized on `jwt_token` for all authentication storage