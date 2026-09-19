// Auth utility functions for consistent session management

export const isAuthenticated = (): boolean => {
    return sessionStorage.getItem('signedIn') === 'true';
};

export const getUserEmail = (): string => {
    return sessionStorage.getItem('user_email') || '';
};

export const getAuthToken = (): string => {
    return sessionStorage.getItem('auth_token') || '';
};

export const getAuthHeaders = (includeJsonContentType = true): Record<string, string> => {
    const headers: Record<string, string> = {};
    const token = getAuthToken();

    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    if (includeJsonContentType) {
        headers['Content-Type'] = 'application/json';
    }

    return headers;
};

export const setAuth = (email: string, token?: string): void => {
    sessionStorage.setItem('signedIn', 'true');
    sessionStorage.setItem('user_email', email);

    if (token) {
        sessionStorage.setItem('auth_token', token);
    }
};

export const clearAuth = (): void => {
    sessionStorage.removeItem('signedIn');
    sessionStorage.removeItem('user_email');
    sessionStorage.removeItem('auth_token');
};
