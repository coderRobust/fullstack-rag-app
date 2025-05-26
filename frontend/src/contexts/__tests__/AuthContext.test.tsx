import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { AuthProvider, useAuth } from '../AuthContext';
import { apiService } from '../../services/api';
import { BrowserRouter } from 'react-router-dom';

vi.mock('../../services/api');
const mockedApiService = apiService as jest.Mocked<typeof apiService>;

const TestComponent = () => {
    const { user, loading, error, login, register, logout } = useAuth();

    return (
        <div>
            {user ? (
                <>
                    <p>Logged in as: {user.email}</p>
                    <button onClick={logout}>Logout</button>
                </>
            ) : (
                <>
                    <button
                        onClick={() => login({ email: 'test@example.com', password: 'password' })}
                        disabled={loading}
                    >
                        Login
                    </button>
                    <button
                        onClick={() =>
                            register({
                                email: 'test@example.com',
                                password: 'password',
                                username: 'testuser',
                            })
                        }
                        disabled={loading}
                    >
                        Register
                    </button>
                </>
            )}
            {error && <p>Error: {error}</p>}
            {loading && <p>Loading...</p>}
        </div>
    );
};

const renderWithRouter = (component: React.ReactNode) => {
    return render(
        <BrowserRouter>
            <AuthProvider>{component}</AuthProvider>
        </BrowserRouter>
    );
};

describe('AuthContext', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        localStorage.clear();
    });

    it('should render login and register buttons when not logged in', () => {
        renderWithRouter(<TestComponent />);
        expect(screen.getByText('Login')).toBeInTheDocument();
        expect(screen.getByText('Register')).toBeInTheDocument();
    });

    it('should handle successful login', async () => {
        const mockUser = { id: 1, email: 'test@example.com', username: 'testuser' };
        const mockResponse = { data: { access_token: 'token', user: mockUser } };
        mockedApiService.post.mockResolvedValueOnce(mockResponse);

        renderWithRouter(<TestComponent />);
        fireEvent.click(screen.getByText('Login'));

        await waitFor(() => {
            expect(screen.getByText(`Logged in as: ${mockUser.email}`)).toBeInTheDocument();
        });
        expect(localStorage.getItem('token')).toBe('token');
    });

    it('should handle login error', async () => {
        const errorMessage = 'Invalid credentials';
        mockedApiService.post.mockRejectedValueOnce(new Error(errorMessage));

        renderWithRouter(<TestComponent />);
        fireEvent.click(screen.getByText('Login'));

        await waitFor(() => {
            expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument();
        });
    });

    it('should handle successful registration', async () => {
        const mockUser = { id: 1, email: 'test@example.com', username: 'testuser' };
        const mockResponse = { data: { access_token: 'token', user: mockUser } };
        mockedApiService.post.mockResolvedValueOnce(mockResponse);

        renderWithRouter(<TestComponent />);
        fireEvent.click(screen.getByText('Register'));

        await waitFor(() => {
            expect(screen.getByText(`Logged in as: ${mockUser.email}`)).toBeInTheDocument();
        });
        expect(localStorage.getItem('token')).toBe('token');
    });

    it('should handle logout', async () => {
        const mockUser = { id: 1, email: 'test@example.com', username: 'testuser' };
        const mockResponse = { data: { access_token: 'token', user: mockUser } };
        mockedApiService.post.mockResolvedValueOnce(mockResponse);

        renderWithRouter(<TestComponent />);
        fireEvent.click(screen.getByText('Login'));

        await waitFor(() => {
            expect(screen.getByText(`Logged in as: ${mockUser.email}`)).toBeInTheDocument();
        });

        fireEvent.click(screen.getByText('Logout'));
        expect(localStorage.getItem('token')).toBeNull();
        expect(screen.getByText('Login')).toBeInTheDocument();
    });
}); 