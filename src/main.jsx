import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { ConfigProvider } from 'antd'
import './index.css'

const theme = {
  token: {
    colorPrimary: '#00D9A3',
    colorBgBase: '#0A0F1E',
    colorTextBase: '#E8EAED',
    borderRadius: 8,
  },
  algorithm: require('antd/lib/theme').darkAlgorithm,
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ConfigProvider theme={theme}>
      <App />
    </ConfigProvider>
  </React.StrictMode>,
)
