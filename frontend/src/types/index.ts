export interface User {
    id: number;
    email: string;
    username: string;
    created_at: string;
    updated_at: string;
}

export interface LoginCredentials {
    email: string;
    password: string;
}

export interface RegisterData extends LoginCredentials {
    username: string;
}

export interface Document {
    id: number;
    title: string;
    content: string;
    metadata: Record<string, any>;
    created_at: string;
    updated_at: string;
}

export interface Question {
    id: number;
    text: string;
    answer: string;
    confidence: number;
    sources: string[];
    created_at: string;
}

export interface ApiResponse<T> {
    data: T;
    message?: string;
    error?: string;
}

export interface PaginatedResponse<T> {
    items: T[];
    total: number;
    page: number;
    size: number;
    pages: number;
}

export interface ApiError {
    message: string;
    code: string;
    details?: Record<string, any>;
} 