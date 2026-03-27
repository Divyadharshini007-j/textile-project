import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, AreaChart, ComposedChart
} from 'recharts';
import { Paper, Typography, Box, useTheme } from '@mui/material';

const PriceTrendChart = ({ data, yarnType }) => {
    const theme = useTheme();

    if (!data || data.length === 0) {
        return (
            <Paper sx={{ p: 4, textAlign: 'center', borderRadius: 3, border: '1px dashed #cbd5e1' }}>
                <Typography color="textSecondary">No price trend data available for <b>{yarnType}</b></Typography>
            </Paper>
        );
    }

    // Prepare display data with separate keys for better Recharts integration
    // This connects the lines at the junction point
    const displayData = data.map((item, index) => {
        const isProjected = item.is_projection;
        const isLastHistorical = !isProjected && (index === data.length - 1 || data[index + 1]?.is_projection);

        return {
            ...item,
            historical_rate: !isProjected || isLastHistorical ? item.rate : null,
            projected_rate: isProjected || isLastHistorical ? item.rate : null
        };
    });

    return (
        <Paper sx={{ p: 3, borderRadius: 3, boxShadow: '0 4px 20px rgba(0,0,0,0.05)' }}>
            <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="h6" sx={{ fontWeight: 700 }}>Market Price Analysis</Typography>
                <Typography variant="caption" sx={{ color: 'textSecondary', bgcolor: '#f1f5f9', px: 1.5, py: 0.5, borderRadius: 10 }}>
                    {yarnType}
                </Typography>
            </Box>

            <Box sx={{ height: { xs: 300, sm: 380 }, width: '100%' }}>
                <ResponsiveContainer>
                    <ComposedChart data={displayData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                        <defs>
                            <linearGradient id="colorRate" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor={theme.palette.primary.main} stopOpacity={0.1} />
                                <stop offset="95%" stopColor={theme.palette.primary.main} stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                        <XAxis
                            dataKey="month"
                            axisLine={false}
                            tickLine={false}
                            tick={{ fontSize: 12, fill: '#64748b' }}
                            dy={10}
                        />
                        <YAxis
                            axisLine={false}
                            tickLine={false}
                            tick={{ fontSize: 12, fill: '#64748b' }}
                            tickFormatter={(val) => `₹${val}`}
                        />
                        <Tooltip
                            contentStyle={{
                                borderRadius: 12,
                                border: 'none',
                                boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)',
                                padding: '12px'
                            }}
                            formatter={(value, name) => [
                                `₹${value.toLocaleString()}`,
                                name === 'historical_rate' ? 'Historical Rate' : 'AI Projection'
                            ]}
                        />
                        <Legend verticalAlign="top" height={36} />

                        <Area
                            type="monotone"
                            dataKey="historical_rate"
                            stroke="none"
                            fillOpacity={1}
                            fill="url(#colorRate)"
                        />

                        <Line
                            type="monotone"
                            dataKey="historical_rate"
                            stroke={theme.palette.primary.main}
                            name="Historical Rate"
                            strokeWidth={3}
                            dot={{ r: 4, strokeWidth: 2, fill: '#fff' }}
                            activeDot={{ r: 6, strokeWidth: 0 }}
                            connectNulls={false}
                        />

                        <Line
                            type="monotone"
                            dataKey="projected_rate"
                            stroke="#10b981"
                            name="AI projection"
                            strokeDasharray="8 5"
                            strokeWidth={3}
                            dot={{ r: 4, strokeWidth: 2, fill: '#fff' }}
                            connectNulls={false}
                        />
                    </ComposedChart>
                </ResponsiveContainer>
            </Box>
            <Box sx={{ mt: 1, display: 'flex', gap: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                    <Box sx={{ width: 12, height: 12, borderRadius: '50%', bgcolor: 'primary.main' }} />
                    <Typography variant="caption" color="textSecondary">Historical</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                    <Box sx={{ width: 12, height: 12, borderRadius: '50%', border: '2px dashed #10b981', bgcolor: 'transparent' }} />
                    <Typography variant="caption" color="textSecondary">Projected (AI)</Typography>
                </Box>
            </Box>
        </Paper>
    );
};

export default PriceTrendChart;
