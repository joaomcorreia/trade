import React, { useState } from 'react';
import {
    Box,
    Container,
    Paper,
    TextField,
    Button,
    Typography,
    Alert,
    InputAdornment,
    IconButton,
    styled,
    ThemeProvider,
    createTheme,
    CssBaseline
} from '@mui/material';
import { Visibility, VisibilityOff, TrendingUp } from '@mui/icons-material';

const theme = createTheme({
    palette: {
        mode: 'dark',
        primary: {
            main: '#00e676',
        },
        secondary: {
            main: '#ff6b6b',
        },
        background: {
            default: '#0a0e27',
            paper: 'rgba(16, 20, 44, 0.95)',
        },
        text: {
            primary: '#ffffff',
            secondary: '#b0bec5',
        },
    },
    typography: {
        fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
        h2: {
            fontWeight: 700,
            letterSpacing: '-0.025em',
        },
        h6: {
            fontWeight: 500,
        },
    },
    components: {
        MuiPaper: {
            styleOverrides: {
                root: {
                    backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                },
            },
        },
        MuiButton: {
            styleOverrides: {
                root: {
                    borderRadius: 12,
                    textTransform: 'none',
                    fontWeight: 600,
                    padding: '12px 32px',
                },
            },
        },
        MuiTextField: {
            styleOverrides: {
                root: {
                    '& .MuiOutlinedInput-root': {
                        borderRadius: 12,
                        backgroundColor: 'rgba(255, 255, 255, 0.05)',
                        '&:hover': {
                            backgroundColor: 'rgba(255, 255, 255, 0.08)',
                        },
                        '&.Mui-focused': {
                            backgroundColor: 'rgba(255, 255, 255, 0.08)',
                        },
                    },
                },
            },
        },
    },
});

const GradientBackground = styled(Box)({
    minHeight: '100vh',
    background: `
        linear-gradient(135deg, #0a0e27 0%, #1a1d3a 50%, #0a0e27 100%),
        radial-gradient(circle at 20% 50%, rgba(0, 230, 118, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(255, 107, 107, 0.15) 0%, transparent 50%)
    `,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    position: 'relative',
    overflow: 'hidden',
    '&::before': {
        content: '""',
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: `
            url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.02'%3E%3Ccircle cx='30' cy='30' r='1'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")
        `,
    },
});

const LoginCard = styled(Paper)(({ theme }) => ({
    padding: theme.spacing(6),
    maxWidth: 420,
    width: '100%',
    margin: theme.spacing(2),
    position: 'relative',
    zIndex: 1,
    boxShadow: '0 20px 40px rgba(0, 0, 0, 0.3)',
}));

const LogoContainer = styled(Box)({
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 32,
    gap: 12,
});

const Logo = styled(TrendingUp)(({ theme }) => ({
    fontSize: 48,
    color: theme.palette.primary.main,
    filter: 'drop-shadow(0 0 10px rgba(0, 230, 118, 0.3))',
}));

interface LoginProps {
    onLogin: (username: string, password: string) => void;
    error?: string;
    loading?: boolean;
}

const Login: React.FC<LoginProps> = ({ onLogin, error, loading = false }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (username.trim() && password.trim()) {
            onLogin(username, password);
        }
    };

    const togglePasswordVisibility = () => {
        setShowPassword(!showPassword);
    };

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <GradientBackground>
                <Container maxWidth="sm">
                    <LoginCard elevation={0}>
                        <LogoContainer>
                            <Logo />
                            <Typography
                                variant="h2"
                                component="h1"
                                sx={{
                                    background: 'linear-gradient(135deg, #00e676 0%, #00c853 100%)',
                                    backgroundClip: 'text',
                                    WebkitBackgroundClip: 'text',
                                    WebkitTextFillColor: 'transparent',
                                }}
                            >
                                JCW
                            </Typography>
                        </LogoContainer>

                        <Typography
                            variant="h6"
                            align="center"
                            sx={{
                                mb: 4,
                                color: 'text.secondary',
                                fontWeight: 300,
                                letterSpacing: '0.1em',
                                textTransform: 'uppercase',
                            }}
                        >
                            TRADE HUB
                        </Typography>

                        {error && (
                            <Alert
                                severity="error"
                                sx={{
                                    mb: 3,
                                    borderRadius: 3,
                                    backgroundColor: 'rgba(255, 107, 107, 0.1)',
                                    border: '1px solid rgba(255, 107, 107, 0.2)',
                                    '& .MuiAlert-icon': {
                                        color: '#ff6b6b',
                                    },
                                }}
                            >
                                {error}
                            </Alert>
                        )}

                        <Box component="form" onSubmit={handleSubmit} sx={{ width: '100%' }}>
                            <TextField
                                fullWidth
                                label="Username"
                                variant="outlined"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                sx={{ mb: 3 }}
                                autoComplete="username"
                                disabled={loading}
                            />

                            <TextField
                                fullWidth
                                label="Password"
                                type={showPassword ? 'text' : 'password'}
                                variant="outlined"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                sx={{ mb: 4 }}
                                autoComplete="current-password"
                                disabled={loading}
                                InputProps={{
                                    endAdornment: (
                                        <InputAdornment position="end">
                                            <IconButton
                                                onClick={togglePasswordVisibility}
                                                edge="end"
                                                disabled={loading}
                                                sx={{ color: 'text.secondary' }}
                                            >
                                                {showPassword ? <VisibilityOff /> : <Visibility />}
                                            </IconButton>
                                        </InputAdornment>
                                    ),
                                }}
                            />

                            <Button
                                type="submit"
                                fullWidth
                                variant="contained"
                                size="large"
                                disabled={!username.trim() || !password.trim() || loading}
                                sx={{
                                    background: 'linear-gradient(135deg, #00e676 0%, #00c853 100%)',
                                    boxShadow: '0 8px 25px rgba(0, 230, 118, 0.3)',
                                    '&:hover': {
                                        background: 'linear-gradient(135deg, #00c853 0%, #00a047 100%)',
                                        boxShadow: '0 12px 35px rgba(0, 230, 118, 0.4)',
                                        transform: 'translateY(-2px)',
                                    },
                                    '&:disabled': {
                                        background: 'rgba(255, 255, 255, 0.1)',
                                        color: 'rgba(255, 255, 255, 0.3)',
                                        boxShadow: 'none',
                                    },
                                    transition: 'all 0.3s ease',
                                }}
                            >
                                {loading ? 'Signing In...' : 'Access Trading Hub'}
                            </Button>
                        </Box>

                        <Typography
                            variant="body2"
                            align="center"
                            sx={{
                                mt: 4,
                                color: 'text.secondary',
                                fontSize: '0.75rem',
                                opacity: 0.7,
                            }}
                        >
                            Authorized Personnel Only
                        </Typography>
                    </LoginCard>
                </Container>
            </GradientBackground>
        </ThemeProvider>
    );
};

export default Login;