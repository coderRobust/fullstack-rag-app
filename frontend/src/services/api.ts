import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import { AuthResponse, Document, Question, Answer, ApiError } from '@/types';

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiService {
    private instance: AxiosInstance;

    constructor() {
        this.instance = axios.create({
            baseURL,
            headers: {
                'Content-Type': 'application/json',
            },
        });

        this.instance.interceptors.request.use(
            (config) => {
                const token = localStorage.getItem('token');
                if (token) {
                    config.headers.Authorization = `Bearer ${token}`;
                }
                return config;
            },
            (error) => Promise.reject(error)
        );

        this.instance.interceptors.response.use(
            (response) => response,
            (error) => {
                if (error.response?.status === 401) {
                    localStorage.removeItem('token');
                    window.location.href = '/login';
                }
                return Promise.reject(this.handleError(error));
            }
        );
    }

    private handleError(error: any): ApiError {
        if (error.response) {
            return {
                message: error.response.data.message || 'An error occurred',
                code: error.response.data.code || 'UNKNOWN_ERROR',
                details: error.response.data.details,
            };
        }
        return {
            message: error.message || 'Network error',
            code: 'NETWORK_ERROR',
        };
    }

    async get<T>(url: string, config?: AxiosRequestConfig) {
        const response = await this.instance.get<T>(url, config);
        return response.data;
    }

    async post<T>(url: string, data?: any, config?: AxiosRequestConfig) {
        const response = await this.instance.post<T>(url, data, config);
        return response.data;
    }

    async put<T>(url: string, data?: any, config?: AxiosRequestConfig) {
        const response = await this.instance.put<T>(url, data, config);
        return response.data;
    }

    async delete<T>(url: string, config?: AxiosRequestConfig) {
        const response = await this.instance.delete<T>(url, config);
        return response.data;
    }

    // Auth endpoints
    async login(email: string, password: string): Promise<AuthResponse> {
        const { data } = await this.post<AuthResponse>('/auth/login', {
            email,
            password,
        });
        return data;
    }

    async register(email: string, password: string): Promise<AuthResponse> {
        const { data } = await this.post<AuthResponse>('/auth/register', {
            email,
            password,
        });
        return data;
    }

    // Document endpoints
    async uploadDocument(file: File, metadata: Record<string, any>): Promise<Document> {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('metadata', JSON.stringify(metadata));

        const { data } = await this.post<Document>('/documents/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return data;
    }

    async getDocuments(): Promise<Document[]> {
        const { data } = await this.get<Document[]>('/documents');
        return data;
    }

    async getDocument(id: number): Promise<Document> {
        const { data } = await this.get<Document>(`/documents/${id}`);
        return data;
    }

    // Q&A endpoints
    async askQuestion(question: Question): Promise<Answer> {
        const { data } = await this.post<Answer>('/qa', question);
        return data;
    }
}

export const apiService = new ApiService(); 