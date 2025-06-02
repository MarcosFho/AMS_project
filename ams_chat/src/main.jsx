import React from 'react';
import ReactDOM from 'react-dom/client';
import AppRoutes from './routes/Routes'; // ✅ importa seu roteador
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AppRoutes /> {/* usa seu sistema de rotas */}
  </React.StrictMode>
);
