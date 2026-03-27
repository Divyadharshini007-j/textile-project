import React, { useState, useEffect } from 'react';
import { AutoGraph as PredictionIcon } from '@mui/icons-material';
import { Grid, Paper, Typography, Box, Card, CardContent, Divider, Stack } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid,
    Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const API_BASE = 'https://textile-project.onrender.com/api';

const DashboardCard = ({ title, value, color, icon, onClick }) => (
    <Card
        sx={{
            height: '100%',
            borderLeft: `5px solid ${color}`,
            cursor: onClick ? 'pointer' : 'default',
            '&:hover': onClick ? { transform: 'scale(1.02)', transition: '0.2s' } : {}
        }}
        onClick={onClick}
    >
        <CardContent>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Box>
                    <Typography color="textSecondary" gutterBottom variant="overline">
                        {title}
                    </Typography>
                    <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
                        {typeof value === 'number'
                            ? value.toLocaleString('en-IN', { style: 'currency', currency: 'INR' })
                            : value}
                    </Typography>
                </Box>
                {icon && <Box sx={{ opacity: 0.3 }}>{icon}</Box>}
            </Stack>
        </CardContent>
    </Card>
);

const Dashboard = () => {
    const [kpis, setKpis] = useState({});
    const [chartData, setChartData] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const kpiRes = await axios.get(`${API_BASE}/dashboard/kpi`);
                setKpis(kpiRes.data || {});
                const chartRes = await axios.get(`${API_BASE}/dashboard/charts`);
                setChartData(chartRes.data.revenue_trend || []);
            } catch (err) {
                console.error("Error fetching dashboard data", err);
            }
        };
        fetchData();
    }, []);

    return (
        <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h4" gutterBottom>Dashboard</Typography>
            <Grid container spacing={3}>
                <Grid item xs={12} sm={6} md={4} lg={4}>
                    <DashboardCard title="Total Sales" value={kpis.total_sales} color="#4caf50" />
                </Grid>
                <Grid item xs={12} sm={6} md={4} lg={4}>
                    <DashboardCard title="Total Purchases" value={kpis.total_purchases} color="#f44336" />
                </Grid>
                <Grid item xs={12} sm={6} md={4} lg={4}>
                    <DashboardCard title="Total Expenses" value={kpis.total_expenses} color="#ff9800" />
                </Grid>
                <Grid item xs={12} sm={6} md={4} lg={4}>
                    <DashboardCard title="Net Profit" value={kpis.net_profit} color="#2196f3" />
                </Grid>
                <Grid item xs={12} sm={6} md={4} lg={4}>
                    <DashboardCard
                        title="AI Insight"
                        value="View Trends"
                        color="#673ab7"
                        icon={<PredictionIcon sx={{ fontSize: 30 }} />}
                        onClick={() => navigate('/predictions')}
                    />
                </Grid>
                <Grid item xs={12} sm={6} md={4} lg={4}>
                    <DashboardCard title="Stock Value" value={kpis.current_stock_value} color="#795548" />
                </Grid>

                <Grid item xs={12} md={8}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6" gutterBottom>Monthly Revenue Trend</Typography>
                        <Box sx={{ height: 300 }}>
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={chartData}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="month" />
                                    <YAxis />
                                    <Tooltip />
                                    <Legend />
                                    <Bar dataKey="total" fill="#8884d8" name="Revenue" />
                                </BarChart>
                            </ResponsiveContainer>
                        </Box>
                    </Paper>
                </Grid>

                <Grid item xs={12} md={4}>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6" gutterBottom>Quick Stats</Typography>
                        <Divider sx={{ my: 1 }} />
                        <Box sx={{ py: 1 }}>
                            <Typography variant="body1">Customer Receivables:</Typography>
                            <Typography variant="h6" color="primary">
                                {kpis.customer_receivables?.toLocaleString('en-IN', { style: 'currency', currency: 'INR' })}
                            </Typography>
                        </Box>
                        <Box sx={{ py: 1 }}>
                            <Typography variant="body1">Supplier Payables:</Typography>
                            <Typography variant="h6" color="secondary">
                                {kpis.supplier_payables?.toLocaleString('en-IN', { style: 'currency', currency: 'INR' })}
                            </Typography>
                        </Box>
                    </Paper>
                </Grid>
            </Grid>
        </Box>
    );
};

export default Dashboard;
