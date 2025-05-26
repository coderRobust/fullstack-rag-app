import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '@/services/api';
import { AuthResponse, User } from '@/types';

interface UseAuthReturn {
    user: User | null;
    isLoading: boolean;
    error: string | null;
    login: (email: string, password: string) => Promise<void>;
    register: (email: string, password: string) => Promise<void>;
    logout: () => void;
}

export const useAuth = (): UseAuthReturn => {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();

    const handleAuthResponse = useCallback((response: AuthResponse) => {
        localStorage.setItem('token', response.accessToken);
        setUser(response.user);
        setError(null);
        navigate('/dashboard');
    }, [navigate]);

    const login = useCallback(async (email: string, password: string) => {
        try {
            setIsLoading(true);
            setError(null);
            const response = await apiService.login(email, password);
            handleAuthResponse(response);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
        } finally {
            setIsLoading(false);
        }
    }, [handleAuthResponse]);

    const register = useCallback(async (email: string, password: string) => {
        try {
            setIsLoading(true);
            setError(null);
            const response = await apiService.register(email, password);
            handleAuthResponse(response);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
        } finally {
            setIsLoading(false);
        }
    }, [handleAuthResponse]);

    const logout = useCallback(() => {
        localStorage.removeItem('token');
        setUser(null);
        navigate('/login');
    }, [navigate]);

    return {
        user,
        isLoading,
        error,
        login,
        register,
        logout,
    };
}; 