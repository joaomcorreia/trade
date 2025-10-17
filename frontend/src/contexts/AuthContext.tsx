import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface AuthContextType {
    isAuthenticated: boolean;
    login: (username: string, password: string) => Promise<boolean>;
    logout: () => void;
    loading: boolean;
    error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

interface AuthProviderProps {
    children: ReactNode;
}

// Simple authentication - you can replace this with your actual auth logic
const VALID_CREDENTIALS = {
    'admin': 'jcwtrade2024',
    'jcw': 'tradehub123',
    'trader': 'secure2024'
};

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        // Check if user is already logged in (from localStorage)
        const token = localStorage.getItem('jcw_auth_token');
        if (token) {
            setIsAuthenticated(true);
        }
    }, []);

    const login = async (username: string, password: string): Promise<boolean> => {
        setLoading(true);
        setError(null);

        try {
            // Simulate API call delay
            await new Promise(resolve => setTimeout(resolve, 1000));

            // Check credentials
            if (VALID_CREDENTIALS[username as keyof typeof VALID_CREDENTIALS] === password) {
                // Generate a simple token (in production, this would come from your backend)
                const token = `jcw_${username}_${Date.now()}`;
                localStorage.setItem('jcw_auth_token', token);
                localStorage.setItem('jcw_username', username);
                setIsAuthenticated(true);
                setLoading(false);
                return true;
            } else {
                setError('Invalid username or password');
                setLoading(false);
                return false;
            }
        } catch (err) {
            setError('Authentication failed. Please try again.');
            setLoading(false);
            return false;
        }
    };

    const logout = () => {
        localStorage.removeItem('jcw_auth_token');
        localStorage.removeItem('jcw_username');
        setIsAuthenticated(false);
        setError(null);
    };

    const value = {
        isAuthenticated,
        login,
        logout,
        loading,
        error
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};