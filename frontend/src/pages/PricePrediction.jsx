import React, { useState, useEffect } from 'react';
import {
    Grid, Paper, Typography, Box, TextField, Button, MenuItem,
    Card, CardContent, CircularProgress, Alert, Stack, Chip, Divider,
    Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
    Accordion, AccordionSummary, AccordionDetails
} from '@mui/material';
import { 
    AutoGraph as PredictionIcon, TrendingUp, TrendingDown, SwapVert, 
    PictureAsPdf as PdfIcon, ExpandMore, Info, History, Analytics
} from '@mui/icons-material';
import axios from 'axios';
import PriceTrendChart from '../components/PriceTrendChart';

const API_BASE = 'http://127.0.0.1:8000/api';

const PricePrediction = () => {
    const [yarnType, setYarnType] = useState('');
    const [availableTypes, setAvailableTypes] = useState([]);
    const [loading, setLoading] = useState(false);
    const [prediction, setPrediction] = useState(null);
    const [trends, setTrends] = useState([]);
    const [historicalData, setHistoricalData] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchTypes = async () => {
            try {
                const res = await axios.get(`${API_BASE}/predictions/yarn-types`);
                setAvailableTypes(res.data);
                if (res.data.length > 0) {
                    setYarnType(res.data[0]);
                }
            } catch (err) {
                console.error("Error fetching yarn types", err);
            }
        };
        fetchTypes();
    }, []);

    const fetchPrediction = async () => {
        if (!yarnType) return;
        setLoading(true);
        setError(null);
        try {
            const predRes = await axios.get(`${API_BASE}/predictions/predict`, {
                params: { yarn_type: yarnType }
            });
            setPrediction(predRes.data);

            const trendRes = await axios.get(`${API_BASE}/predictions/trends`, {
                params: { yarn_type: yarnType }
            });
            setTrends(trendRes.data);

            // Fetch historical data for display
            const historyRes = await axios.get(`${API_BASE}/predictions/historical`, {
                params: { yarn_type: yarnType }
            });
            setHistoricalData(historyRes.data.slice(-10)); // Last 10 records
        } catch (err) {
            console.error("Prediction error", err);
            setError("Failed to fetch predictions. Please ensure the backend is running and data is available.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (yarnType) {
            fetchPrediction();
        }
    }, [yarnType]);

    const getTrendIcon = (trend) => {
        if (trend === 'Rising') return <TrendingUp color="error" />;
        if (trend === 'Falling') return <TrendingDown color="success" />;
        return <SwapVert color="primary" />;
    };

    return (
        <Box sx={{ flexGrow: 1 }}>
            <Stack
                direction={{ xs: 'column', sm: 'row' }}
                alignItems={{ xs: 'flex-start', sm: 'center' }}
                spacing={2}
                sx={{ mb: 4 }}
            >
                <Box sx={{ p: 1, bgcolor: 'primary.main', borderRadius: 2, display: 'flex' }}>
                    <PredictionIcon sx={{ color: 'white', fontSize: 32 }} />
                </Box>
                <Box>
                    <Typography variant="h4" sx={{ fontWeight: 700 }}>AI Price Analytics</Typography>
                    <Typography variant="body2" color="textSecondary">Smart market forecasting for textile procurement</Typography>
                </Box>
            </Stack>

            <Grid container spacing={4}>
                <Grid item xs={12} lg={4}>
                    <Paper sx={{ p: 3, borderRadius: 3, boxShadow: '0 4px 20px rgba(0,0,0,0.08)' }}>
                        <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                            <Box component="span" sx={{ mr: 1, width: 4, height: 24, bgcolor: 'primary.main', borderRadius: 1 }} />
                            Analysis Parameters
                        </Typography>
                        <Stack spacing={3} sx={{ mt: 2 }}>
                            <TextField
                                select
                                label="Yarn Type"
                                value={yarnType}
                                onChange={(e) => setYarnType(e.target.value)}
                                fullWidth
                                variant="outlined"
                            >
                                {availableTypes.map((type) => (
                                    <MenuItem key={type} value={type}>{type}</MenuItem>
                                ))}
                            </TextField>

                            <Box sx={{ p: 2, bgcolor: 'info.light', borderRadius: 2 }}>
                                <Typography variant="body2" color="info.dark" sx={{ fontWeight: 600 }}>
                                    <Info sx={{ fontSize: 16, verticalAlign: 'middle', mr: 1 }} />
                                    Price Prediction Basis
                                </Typography>
                                <Typography variant="caption" color="info.dark">
                                    • Price per kg based on historical purchases
                                    • Based on {prediction?.history_count || 0} historical data points
                                    • Shows market trend and future predictions
                                    • Simple linear trend analysis
                                </Typography>
                            </Box>

                            <Button
                                variant="contained"
                                size="large"
                                onClick={fetchPrediction}
                                disabled={loading || !yarnType}
                                sx={{ py: 1.5, borderRadius: 2 }}
                                startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <PredictionIcon />}
                            >
                                Get Price Prediction
                            </Button>
                        </Stack>
                    </Paper>

                    {prediction && (
                        <Card sx={{
                            mt: 3,
                            borderRadius: 3,
                            background: prediction.trend === 'Rising'
                                ? 'linear-gradient(135deg, #fff5f5 0%, #ffe3e3 100%)'
                                : prediction.trend === 'Falling'
                                    ? 'linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%)'
                                    : 'linear-gradient(135deg, #f0f7ff 0%, #e0efff 100%)',
                            boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
                            border: '1px solid rgba(255,255,255,0.3)'
                        }}>
                            <CardContent sx={{ p: 3 }}>
                                <Typography variant="overline" color="textSecondary" sx={{ fontSize: 12, fontWeight: 600 }}>
                                    Current Market Price (per kg)
                                </Typography>
                                <Typography variant="h3" sx={{
                                    color: prediction.trend === 'Rising' ? '#d32f2f' : prediction.trend === 'Falling' ? '#2e7d32' : 'primary.main',
                                    fontWeight: 800,
                                    my: 1
                                }}>
                                    ₹{prediction.predicted_price.toLocaleString()}/kg
                                </Typography>

                                <Divider sx={{ my: 2, opacity: 0.6 }} />

                                <Grid container spacing={2}>
                                    <Grid item xs={6}>
                                        <Typography variant="caption" color="textSecondary">Historical Avg</Typography>
                                        <Typography variant="body1" sx={{ fontWeight: 600 }}>
                                            ₹{prediction.historical_avg?.toLocaleString() || 'N/A'}/kg
                                        </Typography>
                                    </Grid>
                                    <Grid item xs={6}>
                                        <Typography variant="caption" color="textSecondary">Market Trend</Typography>
                                        <Stack direction="row" alignItems="center" spacing={0.5}>
                                            {getTrendIcon(prediction.trend)}
                                            <Typography variant="body1" sx={{ fontWeight: 600, color: prediction.trend === 'Rising' ? '#d32f2f' : prediction.trend === 'Falling' ? '#2e7d32' : 'inherit' }}>
                                                {prediction.trend}
                                            </Typography>
                                        </Stack>
                                    </Grid>
                                </Grid>

                                <Box sx={{ mt: 3 }}>
                                    <Typography variant="subtitle2" color="primary" gutterBottom sx={{ fontWeight: 700 }}>
                                        3-Month Price Forecast (per kg)
                                    </Typography>
                                    {prediction.three_month_prediction && prediction.three_month_prediction.length > 0 ? (
                                        <Stack spacing={1}>
                                            {prediction.three_month_prediction.map((month, index) => (
                                                <Box key={index} sx={{ 
                                                    display: 'flex', 
                                                    justifyContent: 'space-between', 
                                                    alignItems: 'center',
                                                    p: 1,
                                                    bgcolor: 'background.paper',
                                                    borderRadius: 1,
                                                    border: '1px solid rgba(0,0,0,0.1)'
                                                }}>
                                                    <Typography variant="body2" sx={{ fontWeight: 500 }}>
                                                        {month.month}
                                                    </Typography>
                                                    <Typography variant="body2" sx={{ fontWeight: 700, color: 'primary.main' }}>
                                                        ₹{month.predicted_price.toLocaleString()}/kg
                                                    </Typography>
                                                </Box>
                                            ))}
                                        </Stack>
                                    ) : (
                                        <Typography variant="body2" color="textSecondary" sx={{ p: 2, textAlign: 'center', bgcolor: 'grey.50', borderRadius: 1 }}>
                                            No future predictions available (insufficient historical data)
                                        </Typography>
                                    )}
                                </Box>

                                <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 2 }}>
                                    <Chip
                                        label={prediction.confidence}
                                        size="small"
                                        color={prediction.confidence.includes('High') ? "success" : prediction.confidence.includes('Medium') ? "warning" : "error"}
                                        sx={{ fontWeight: 600, px: 1 }}
                                    />
                                    <Button
                                        variant="outlined"
                                        size="small"
                                        startIcon={<PdfIcon />}
                                        onClick={() => window.open(`${API_BASE}/reports/prediction?yarn_type=${yarnType}`, '_blank')}
                                        sx={{ borderRadius: 2, textTransform: 'none', fontWeight: 600 }}
                                    >
                                        Export Report
                                    </Button>
                                </Box>
                                <Typography variant="caption" display="block" sx={{ mt: 1, color: 'textSecondary', textAlign: 'right', fontStyle: 'italic' }}>
                                    Based on {prediction.history_count} historical purchases
                                </Typography>
                            </CardContent>
                        </Card>
                    )}

                    {/* Historical Data Display */}
                    {historicalData.length > 0 && (
                        <Accordion sx={{ mt: 3 }}>
                            <AccordionSummary expandIcon={<ExpandMore />}>
                                <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center' }}>
                                    <History sx={{ mr: 1 }} />
                                    Historical Data (Last 10 Purchases)
                                </Typography>
                            </AccordionSummary>
                            <AccordionDetails>
                                <TableContainer sx={{ maxHeight: 300 }}>
                                    <Table size="small" stickyHeader>
                                        <TableHead>
                                            <TableRow>
                                                <TableCell>Date</TableCell>
                                                <TableCell>Quantity (kg)</TableCell>
                                                <TableCell align="right">Rate/kg</TableCell>
                                                <TableCell align="right">Total</TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {historicalData.map((record, index) => (
                                                <TableRow key={index}>
                                                    <TableCell>
                                                        {new Date(record.date).toLocaleDateString()}
                                                    </TableCell>
                                                    <TableCell>{record.quantity}</TableCell>
                                                    <TableCell align="right">
                                                        ₹{record.rate.toLocaleString()}/kg
                                                    </TableCell>
                                                    <TableCell align="right">
                                                        ₹{(record.rate * record.quantity).toLocaleString()}
                                                    </TableCell>
                                                </TableRow>
                                            ))}
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                            </AccordionDetails>
                        </Accordion>
                    )}
                </Grid>

                <Grid item xs={12} lg={8}>
                    {error && <Alert severity="error" sx={{ mb: 2, borderRadius: 2 }}>{error}</Alert>}
                    <PriceTrendChart data={trends} yarnType={yarnType} />

                    <Paper sx={{ mt: 3, p: 3, borderRadius: 3, bgcolor: '#f8fafc' }}>
                        <Typography variant="subtitle2" color="primary" gutterBottom sx={{ fontWeight: 700, display: 'flex', alignItems: 'center' }}>
                            <Analytics sx={{ mr: 1 }} />
                            Prediction Methodology
                        </Typography>
                        <Grid container spacing={2}>
                            <Grid item xs={12} sm={6}>
                                <Typography variant="body2">
                                    <strong>Basis:</strong> Historical purchase prices per kg<br/>
                                    <strong>Analysis:</strong> Simple linear trend analysis<br/>
                                    <strong>Data:</strong> All available historical purchases<br/>
                                    <strong>Accuracy:</strong> Based on data quality
                                </Typography>
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <Typography variant="body2">
                                    <strong>Current Price:</strong> Recent market average<br/>
                                    <strong>Forecast:</strong> 3-month future predictions<br/>
                                    <strong>Trend:</strong> Rising/Falling/Stable based on recent data<br/>
                                    <strong>Confidence:</strong> High/Medium/Low based on data points
                                </Typography>
                            </Grid>
                        </Grid>
                        
                        <Box sx={{ mt: 2, p: 2, bgcolor: 'white', borderRadius: 2, border: '1px solid #e0e0e0' }}>
                            <Typography variant="body2" color="textSecondary">
                                <strong>Simple & Clear:</strong> Prices are shown per kg based on historical purchase data. 
                                Future predictions use simple trend analysis. No complex algorithms - just straightforward market analysis.
                            </Typography>
                        </Box>
                    </Paper>
                </Grid>
            </Grid>
        </Box>
    );
};

export default PricePrediction;
