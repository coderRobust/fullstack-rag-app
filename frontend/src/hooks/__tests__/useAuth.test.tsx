import { renderHook, act } from '@testing-library/react';
import { useAuth } from '../useAuth';
import { apiService } from '@/services/api';
import { AuthResponse } from '@/types';

// Mock the apiService
jest.mock('@/services/api', () => ({
    apiService: {
        login: jest.fn(),
        register: jest.fn(),
    },
}));

// Mock react-router-dom
jest.mock('react-router-dom', () => ({
    useNavigate: () => jest.fn(),
}));

describe('useAuth', () => {
    const mockUser = {
        id: 1,
        email: 'test@example.com',
        isActive: true,
        createdAt: '2024-03-20T10:00:00Z',
        updatedAt: '2024-03-20T10:00:00Z',
    };

    const mockAuthResponse: AuthResponse = {
        accessToken: 'mock-token',
        tokenType: 'bearer',
        user: mockUser,
    };

    beforeEach(() => {
        localStorage.clear();
        jest.clearAllMocks();
    });

    it('should handle login successfully', async () => {
        (apiService.login as jest.Mock).mockResolvedValueOnce(mockAuthResponse);

        const { result } = renderHook(() => useAuth());

        await act(async () => {
            await result.current.login('test@example.com', 'password');
        });

        expect(result.current.user).toEqual(mockUser);
        expect(result.current.error).toBeNull();
        expect(localStorage.getItem('token')).toBe('mock-token');
    });

    it('should handle login error', async () => {
        const errorMessage = 'Invalid credentials';
        (apiService.login as jest.Mock).mockRejectedValueOnce(new Error(errorMessage));

        const { result } = renderHook(() => useAuth());

        await act(async () => {
            await result.current.login('test@example.com', 'wrong-password');
        });

        expect(result.current.user).toBeNull();
        expect(result.current.error).toBe(errorMessage);
        expect(localStorage.getItem('token')).toBeNull();
    });

    it('should handle register successfully', async () => {
        (apiService.register as jest.Mock).mockResolvedValueOnce(mockAuthResponse);

        const { result } = renderHook(() => useAuth());

        await act(async () => {
            await result.current.register('test@example.com', 'password');
        });

        expect(result.current.user).toEqual(mockUser);
        expect(result.current.error).toBeNull();
        expect(localStorage.getItem('token')).toBe('mock-token');
    });

    it('should handle logout', () => {
        localStorage.setItem('token', 'mock-token');
        const { result } = renderHook(() => useAuth());

        act(() => {
            result.current.logout();
        });

        expect(result.current.user).toBeNull();
        expect(localStorage.getItem('token')).toBeNull();
    });
}); 