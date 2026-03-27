import React, { useState, useEffect } from 'react';
import { 
    Box, Typography, Button, Paper, Grid, Card, CardContent, 
    CircularProgress, Alert, Chip, Avatar, LinearProgress,
    Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
    useTheme, alpha
} from '@mui/material';
import { 
    PictureAsPdf as PdfIcon, TrendingUp, TrendingDown, 
    Inventory, AttachMoney, Assessment, Download,
    People, ShoppingCart, Store, AccountBalance
} from '@mui/icons-material';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000/api';

const Reports = () => {
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const theme = useTheme();

    useEffect(() => {
        fetchDashboardData();
    }, []);

    const fetchDashboardData = async () => {
        try {
            const [sales, purchases, inventory, expenses] = await Promise.all([
                axios.get(`${API_BASE}/sales/`),
                axios.get(`${API_BASE}/purchases/`),
                axios.get(`${API_BASE}/inventory/`),
                axios.get(`${API_BASE}/expenses/`)
            ]);

            const totalSales = sales.data.reduce((sum, sale) => sum + (sale.grand_total || 0), 0);
            const totalPurchases = purchases.data.reduce((sum, purchase) => sum + (purchase.grand_total || 0), 0);
            const totalExpenses = expenses.data.reduce((sum, expense) => sum + (expense.amount || 0), 0);
            const totalInventoryValue = inventory.data.reduce((sum, item) => sum + (item.total_value || 0), 0);
            const netProfit = (totalSales + totalInventoryValue) - (totalPurchases + totalExpenses);

            setDashboardData({
                totalSales,
                totalPurchases,
                totalExpenses,
                totalInventoryValue,
                netProfit,
                totalTransactions: sales.data.length + purchases.data.length,
                lowStockItems: inventory.data.filter(item => (item.quantity || 0) < 50).length,
                recentSales: sales.data.slice(0, 3),
                recentPurchases: purchases.data.slice(0, 3),
                topInventory: inventory.data.sort((a, b) => (b.total_value || 0) - (a.total_value || 0)).slice(0, 5)
            });
        } catch (err) {
            console.error('Failed to fetch dashboard data:', err);
            setError('Failed to load dashboard data');
        } finally {
            setLoading(false);
        }
    };

    const handleDownload = (type) => {
        window.open(`http://127.0.0.1:8000/api/reports/${type}`, '_blank');
    };

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
                <CircularProgress />
            </Box>
        );
    }

    if (error) {
        return (
            <Box>
                <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>
                <Typography variant="h4" gutterBottom>Business Reports</Typography>
            </Box>
        );
    }

    const profitPercentage = dashboardData.totalSales > 0 
        ? ((dashboardData.netProfit / dashboardData.totalSales) * 100).toFixed(1)
        : 0;

    return (
        <Box sx={{ flexGrow: 1, p: { xs: 1, sm: 2, md: 3 } }}>
            {/* Header */}
            <Box sx={{ mb: 4, textAlign: { xs: 'center', md: 'left' } }}>
                <Typography variant="h3" fontWeight="bold" color="primary" gutterBottom>
                    Business Analytics
                </Typography>
                <Typography variant="h6" color="textSecondary">
                    Real-time insights and financial reports for your textile business
                </Typography>
            </Box>

            {/* Key Metrics Cards */}
            <Grid container spacing={{ xs: 2, sm: 3 }} sx={{ mb: 4 }}>
                <Grid item xs={12} sm={6} lg={3}>
                    <Card 
                        elevation={4}
                        sx={{ 
                            background: dashboardData?.netProfit >= 0 
                                ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                                : 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                            color: 'white',
                            borderRadius: 3,
                            transform: { xs: 'scale(1)', md: 'scale(1)' },
                            transition: 'transform 0.2s'
                        }}
                    >
                        <CardContent sx={{ p: { xs: 2, md: 3 } }}>
                            <Box display="flex" alignItems="center" justifyContent="space-between">
                                <Box>
                                    <Typography variant="h6" sx={{ fontSize: { xs: '0.9rem', md: '1rem' } }}>
                                        Net Profit
                                    </Typography>
                                    <Typography variant="h4" fontWeight="bold" sx={{ fontSize: { xs: '1.5rem', md: '2rem' } }}>
                                        ₹{dashboardData?.netProfit?.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                                    </Typography>
                                    <Typography variant="caption" sx={{ opacity: 0.9 }}>
                                        {profitPercentage}% margin
                                    </Typography>
                                </Box>
                                <Avatar sx={{ 
                                    bgcolor: 'rgba(255,255,255,0.2)', 
                                    width: { xs: 40, md: 56 }, 
                                    height: { xs: 40, md: 56 } 
                                }}>
                                    {dashboardData?.netProfit >= 0 ? <TrendingUp /> : <TrendingDown />}
                                </Avatar>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} sm={6} lg={3}>
                    <Card 
                        elevation={4}
                        sx={{ 
                            background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
                            color: 'white',
                            borderRadius: 3
                        }}
                    >
                        <CardContent sx={{ p: { xs: 2, md: 3 } }}>
                            <Box display="flex" alignItems="center" justifyContent="space-between">
                                <Box>
                                    <Typography variant="h6" sx={{ fontSize: { xs: '0.9rem', md: '1rem' } }}>
                                        Total Sales
                                    </Typography>
                                    <Typography variant="h4" fontWeight="bold" sx={{ fontSize: { xs: '1.5rem', md: '2rem' } }}>
                                        ₹{dashboardData?.totalSales?.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                                    </Typography>
                                    <Typography variant="caption" sx={{ opacity: 0.9 }}>
                                        Revenue this period
                                    </Typography>
                                </Box>
                                <Avatar sx={{ 
                                    bgcolor: 'rgba(255,255,255,0.2)', 
                                    width: { xs: 40, md: 56 }, 
                                    height: { xs: 40, md: 56 } 
                                }}>
                                    <AttachMoney />
                                </Avatar>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} sm={6} lg={3}>
                    <Card 
                        elevation={4}
                        sx={{ 
                            background: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
                            color: '#333',
                            borderRadius: 3
                        }}
                    >
                        <CardContent sx={{ p: { xs: 2, md: 3 } }}>
                            <Box display="flex" alignItems="center" justifyContent="space-between">
                                <Box>
                                    <Typography variant="h6" sx={{ fontSize: { xs: '0.9rem', md: '1rem' } }}>
                                        Inventory Value
                                    </Typography>
                                    <Typography variant="h4" fontWeight="bold" sx={{ fontSize: { xs: '1.5rem', md: '2rem' } }}>
                                        ₹{dashboardData?.totalInventoryValue?.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                                    </Typography>
                                    <Typography variant="caption" sx={{ opacity: 0.7 }}>
                                        Current stock worth
                                    </Typography>
                                </Box>
                                <Avatar sx={{ 
                                    bgcolor: 'rgba(255,255,255,0.5)', 
                                    width: { xs: 40, md: 56 }, 
                                    height: { xs: 40, md: 56 } 
                                }}>
                                    <Inventory />
                                </Avatar>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} sm={6} lg={3}>
                    <Card 
                        elevation={4}
                        sx={{ 
                            background: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
                            color: '#333',
                            borderRadius: 3
                        }}
                    >
                        <CardContent sx={{ p: { xs: 2, md: 3 } }}>
                            <Box display="flex" alignItems="center" justifyContent="space-between">
                                <Box>
                                    <Typography variant="h6" sx={{ fontSize: { xs: '0.9rem', md: '1rem' } }}>
                                        Transactions
                                    </Typography>
                                    <Typography variant="h4" fontWeight="bold" sx={{ fontSize: { xs: '1.5rem', md: '2rem' } }}>
                                        {dashboardData?.totalTransactions}
                                    </Typography>
                                    <Typography variant="caption" sx={{ opacity: 0.7 }}>
                                        Total operations
                                    </Typography>
                                </Box>
                                <Avatar sx={{ 
                                    bgcolor: 'rgba(255,255,255,0.5)', 
                                    width: { xs: 40, md: 56 }, 
                                    height: { xs: 40, md: 56 } 
                                }}>
                                    <Assessment />
                                </Avatar>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            {/* Reports Section */}
            <Grid container spacing={{ xs: 2, sm: 3 }}>
                <Grid item xs={12} lg={8}>
                    <Paper elevation={3} sx={{ borderRadius: 3, p: { xs: 2, md: 3 } }}>
                        <Box display="flex" alignItems="center" justifyContent="space-between" mb={3}>
                            <Typography variant="h5" fontWeight="bold">
                                📊 Financial Reports
                            </Typography>
                            <Chip 
                                label="PDF Downloads" 
                                color="primary" 
                                size="small" 
                                icon={<Download />}
                            />
                        </Box>
                        
                        <Grid container spacing={2}>
                            <Grid item xs={12} sm={6}>
                                <Button
                                    fullWidth
                                    variant="contained"
                                    startIcon={<PdfIcon />}
                                    onClick={() => handleDownload('profit-loss')}
                                    sx={{ 
                                        py: 2, 
                                        borderRadius: 2,
                                        background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                                        fontSize: { xs: '0.8rem', md: '0.9rem' }
                                    }}
                                >
                                    Profit & Loss Statement
                                </Button>
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <Button
                                    fullWidth
                                    variant="contained"
                                    startIcon={<PdfIcon />}
                                    onClick={() => handleDownload('stock-valuation')}
                                    sx={{ 
                                        py: 2, 
                                        borderRadius: 2,
                                        background: 'linear-gradient(45deg, #FF6B6B 30%, #FFE66D 90%)',
                                        fontSize: { xs: '0.8rem', md: '0.9rem' }
                                    }}
                                >
                                    Stock Valuation Report
                                </Button>
                            </Grid>
                        </Grid>
                    </Paper>
                </Grid>

                <Grid item xs={12} lg={4}>
                    <Paper elevation={3} sx={{ borderRadius: 3, p: { xs: 2, md: 3 } }}>
                        <Typography variant="h5" fontWeight="bold" mb={3}>
                            📈 Quick Stats
                        </Typography>
                        
                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                            <Box>
                                <Typography variant="body2" color="textSecondary">Low Stock Items</Typography>
                                <Typography variant="h6" fontWeight="bold" color="error">
                                    {dashboardData?.lowStockItems || 0} items
                                </Typography>
                            </Box>
                            
                            <Box>
                                <Typography variant="body2" color="textSecondary">Total Expenses</Typography>
                                <Typography variant="h6" fontWeight="bold" color="text.primary">
                                    ₹{dashboardData?.totalExpenses?.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                                </Typography>
                            </Box>
                            
                            <Box>
                                <Typography variant="body2" color="textSecondary">Total Purchases</Typography>
                                <Typography variant="h6" fontWeight="bold" color="text.primary">
                                    ₹{dashboardData?.totalPurchases?.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                                </Typography>
                            </Box>
                        </Box>
                    </Paper>
                </Grid>
            </Grid>

            {/* Recent Activity Tables */}
            <Grid container spacing={{ xs: 2, sm: 3 }} sx={{ mt: 2 }}>
                <Grid item xs={12} md={6}>
                    <Paper elevation={3} sx={{ borderRadius: 3, p: { xs: 2, md: 3 } }}>
                        <Typography variant="h6" fontWeight="bold" mb={2}>
                            🛒 Recent Sales
                        </Typography>
                        {dashboardData?.recentSales?.length > 0 ? (
                            <TableContainer>
                                <Table size="small">
                                    <TableHead>
                                        <TableRow>
                                            <TableCell>Date</TableCell>
                                            <TableCell>Customer ID</TableCell>
                                            <TableCell align="right">Amount</TableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                        {dashboardData.recentSales.map((sale, index) => (
                                            <TableRow key={index}>
                                                <TableCell>
                                                    {sale.date ? new Date(sale.date).toLocaleDateString() : 'N/A'}
                                                </TableCell>
                                                <TableCell>{sale.customer_id}</TableCell>
                                                <TableCell align="right">
                                                    ₹{sale.grand_total?.toLocaleString('en-IN')}
                                                </TableCell>
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                </Table>
                            </TableContainer>
                        ) : (
                            <Typography variant="body2" color="textSecondary" textAlign="center" py={2}>
                                No recent sales
                            </Typography>
                        )}
                    </Paper>
                </Grid>

                <Grid item xs={12} md={6}>
                    <Paper elevation={3} sx={{ borderRadius: 3, p: { xs: 2, md: 3 } }}>
                        <Typography variant="h6" fontWeight="bold" mb={2}>
                            📦 Recent Purchases
                        </Typography>
                        {dashboardData?.recentPurchases?.length > 0 ? (
                            <TableContainer>
                                <Table size="small">
                                    <TableHead>
                                        <TableRow>
                                            <TableCell>Date</TableCell>
                                            <TableCell>Supplier ID</TableCell>
                                            <TableCell align="right">Amount</TableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                        {dashboardData.recentPurchases.map((purchase, index) => (
                                            <TableRow key={index}>
                                                <TableCell>
                                                    {purchase.date ? new Date(purchase.date).toLocaleDateString() : 'N/A'}
                                                </TableCell>
                                                <TableCell>{purchase.supplier_id}</TableCell>
                                                <TableCell align="right">
                                                    ₹{purchase.grand_total?.toLocaleString('en-IN')}
                                                </TableCell>
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                </Table>
                            </TableContainer>
                        ) : (
                            <Typography variant="body2" color="textSecondary" textAlign="center" py={2}>
                                No recent purchases
                            </Typography>
                        )}
                    </Paper>
                </Grid>
            </Grid>
        </Box>
    );
};

export default Reports;
