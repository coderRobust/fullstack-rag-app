import { describe, it, expect, vi, beforeEach } from 'vitest';
import { apiService } from '../api';
import axios from 'axios';

vi.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('ApiService', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        localStorage.clear();
    });

    it('should make a GET request', async () => {
        const mockResponse = { data: { id: 1, name: 'Test' } };
        mockedAxios.create.mockReturnValue({
            get: vi.fn().mockResolvedValue(mockResponse),
        } as any);

        const result = await apiService.get('/test');
        expect(result).toEqual(mockResponse.data);
    });

    it('should make a POST request', async () => {
        const mockResponse = { data: { id: 1, name: 'Test' } };
        mockedAxios.create.mockReturnValue({
            post: vi.fn().mockResolvedValue(mockResponse),
        } as any);

        const result = await apiService.post('/test', { name: 'Test' });
        expect(result).toEqual(mockResponse.data);
    });

    it('should add auth token to requests', async () => {
        const token = 'test-token';
        localStorage.setItem('token', token);

        const mockAxiosInstance = {
            interceptors: {
                request: {
                    use: vi.fn(),
                },
                response: {
                    use: vi.fn(),
                },
            },
        };

        mockedAxios.create.mockReturnValue(mockAxiosInstance as any);

        new apiService.constructor();

        const requestInterceptor = mockAxiosInstance.interceptors.request.use.mock.calls[0][0];
        const config = { headers: {} };
        const result = requestInterceptor(config);

        expect(result.headers.Authorization).toBe(`Bearer ${token}`);
    });

    it('should handle 401 errors', async () => {
        const mockAxiosInstance = {
            interceptors: {
                request: {
                    use: vi.fn(),
                },
                response: {
                    use: vi.fn(),
                },
            },
        };

        mockedAxios.create.mockReturnValue(mockAxiosInstance as any);

        new apiService.constructor();

        const responseInterceptor = mockAxiosInstance.interceptors.response.use.mock.calls[0][1];
        const error = { response: { status: 401 } };

        await responseInterceptor(error);

        expect(localStorage.getItem('token')).toBeNull();
    });

    it('should handle network errors', async () => {
        const mockAxiosInstance = {
            interceptors: {
                request: {
                    use: vi.fn(),
                },
                response: {
                    use: vi.fn(),
                },
            },
        };

        mockedAxios.create.mockReturnValue(mockAxiosInstance as any);

        new apiService.constructor();

        const responseInterceptor = mockAxiosInstance.interceptors.response.use.mock.calls[0][1];
        const error = { message: 'Network Error' };

        const result = await responseInterceptor(error);

        expect(result).rejects.toEqual({
            message: 'Network Error',
            code: 'NETWORK_ERROR',
        });
    });
}); 