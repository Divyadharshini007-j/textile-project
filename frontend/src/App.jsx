import React, { useState } from 'react';
import {
  Box, Drawer, AppBar, Toolbar, List, Typography, Divider,
  IconButton, ListItem, ListItemIcon, ListItemText, Container, CssBaseline, Button
} from '@mui/material';
import {
  Menu as MenuIcon, Dashboard as DashboardIcon,
  ShoppingBag as ShoppingIcon, PointOfSale as SaleIcon,
  AttachMoney as ExpenseIcon, People as PeopleIcon,
  Storage as StorageIcon, Assessment as ReportIcon,
  AutoGraph as PredictionIcon, Work as HiringIcon
} from '@mui/icons-material';
import { Routes, Route, useNavigate, Navigate } from 'react-router-dom';

// Main app pages
import Dashboard from './pages/Dashboard';
import Purchases from './pages/Purchases';
import Sales from './pages/Sales';
import Login from './pages/Login';
import Conversions from './pages/Conversions';
import Inventory from './pages/Inventory';
import Reports from './pages/Reports';
import PricePrediction from './pages/PricePrediction';
import Customers from './pages/Customers';
import Suppliers from './pages/Suppliers';
import Expenses from './pages/Expenses';

// Hiring pages (standalone, no sidebar)
import WorkerRegister from './pages/WorkerRegister';
import WorkerLogin from './pages/WorkerLogin';
import WorkerDashboard from './pages/WorkerDashboard';
import AdminHiring from './pages/AdminHiring';

const drawerWidth = 240;

// Protected route: redirects to /worker/login if no worker token
const ProtectedWorkerRoute = ({ children }) => {
  return localStorage.getItem('worker_token')
    ? children
    : <Navigate to="/worker/login" replace />;
};

function App() {
  const navigate = useNavigate();
  const [open, setOpen] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('token'));

  // Worker & Admin Hiring routes render standalone (no sidebar)
  // We check path prefix to decide layout
  const path = window.location.pathname;
  const isWorkerRoute = path.startsWith('/worker/');
  const isAdminHiringRoute = path === '/admin/hiring';

  if (isWorkerRoute || isAdminHiringRoute) {
    return (
      <Routes>
        <Route path="/worker/login" element={<WorkerLogin />} />
        <Route path="/worker/register" element={<WorkerRegister />} />
        <Route path="/worker/dashboard" element={
          <ProtectedWorkerRoute><WorkerDashboard /></ProtectedWorkerRoute>
        } />
        <Route path="/admin/hiring" element={<AdminHiring />} />
        <Route path="*" element={<Navigate to="/worker/login" replace />} />
      </Routes>
    );
  }

  // Main app: requires main token
  if (!token) {
    return <Login onLogin={(t) => setToken(t)} />;
  }

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('main_user');
    setToken(null);
  };

  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
    { text: 'Purchases', icon: <ShoppingIcon />, path: '/purchases' },
    { text: 'Sales', icon: <SaleIcon />, path: '/sales' },
    { text: 'Conversions', icon: <StorageIcon />, path: '/conversions' },
    { text: 'Customers', icon: <PeopleIcon />, path: '/customers' },
    { text: 'Suppliers', icon: <StorageIcon />, path: '/suppliers' },
    { text: 'Expenses', icon: <ExpenseIcon />, path: '/expenses' },
    { text: 'Reports', icon: <ReportIcon />, path: '/reports' },
    { text: 'AI Predictions', icon: <PredictionIcon />, path: '/predictions' },
  ];

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <IconButton color="inherit" onClick={() => setOpen(!open)} edge="start" sx={{ mr: 2 }}>
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            Yarn Trading Accountancy
          </Typography>
          {/* Quick link to hiring portal */}
          <Button
            color="inherit"
            startIcon={<HiringIcon />}
            onClick={() => window.open('/admin/hiring', '_blank')}
            sx={{ mr: 2, opacity: 0.85 }}
            size="small"
          >
            Hiring Portal
          </Button>
          <Button color="inherit" onClick={handleLogout}>Logout</Button>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <List>
            {menuItems.map((item) => (
              <ListItem
                button key={item.text}
                onClick={() => navigate(item.path)}
                selected={window.location.pathname === item.path}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItem>
            ))}
          </List>
          <Divider />
          <List>
            <ListItem button="true" onClick={() => window.open('/admin/hiring', '_blank')}>
              <ListItemIcon><HiringIcon color="primary" /></ListItemIcon>
              <ListItemText primary="Worker Hiring" secondary="Admin Portal" />
            </ListItem>
            <ListItem button="true" onClick={() => window.open('/worker/login', '_blank')}>
              <ListItemIcon><HiringIcon /></ListItemIcon>
              <ListItemText primary="Worker Login" secondary="Worker Portal" />
            </ListItem>
          </List>
        </Box>
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        <Container maxWidth={false}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/purchases" element={<Purchases />} />
            <Route path="/sales" element={<Sales />} />
            <Route path="/inventory" element={<Inventory />} />
            <Route path="/conversions" element={<Conversions />} />
            <Route path="/customers" element={<Customers />} />
            <Route path="/suppliers" element={<Suppliers />} />
            <Route path="/expenses" element={<Expenses />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/predictions" element={<PricePrediction />} />
            <Route path="*" element={<div>Page not found.</div>} />
          </Routes>
        </Container>
      </Box>
    </Box>
  );
}

export default App;
