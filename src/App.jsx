import React, { useState } from 'react'
import { Layout, Menu, Card } from 'antd'
import { BgColorsOutlined, InfoCircleOutlined, QuestionCircleOutlined } from '@ant-design/icons'
import DetectionPage from './pages/DetectionPage'
import AboutPage from './pages/AboutPage'
import HelpPage from './pages/HelpPage'

const { Sider, Content, Header } = Layout

export default function App() {
  const [page, setPage] = useState('detection')

  const renderPage = () => {
    switch (page) {
      case 'detection':
        return <DetectionPage />
      case 'about':
        return <AboutPage />
      case 'help':
        return <HelpPage />
      default:
        return <DetectionPage />
    }
  }

  return (
    <Layout className="agriguard-layout" style={{ minHeight: '100vh' }}>
      <Sider
        width={250}
        style={{
          background: 'linear-gradient(180deg, #0F1624 0%, #131B2E 100%)',
          borderRight: '1px solid #2A3B52',
        }}
      >
        <div style={{ padding: '2rem 1.5rem', textAlign: 'center' }}>
          <h2 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>🌿 AgriGuard</h2>
          <p style={{ color: '#B4B8BE', marginBottom: 0, fontSize: '0.875rem' }}>
            AI-Powered Plant Disease Detection
          </p>
        </div>

        <Menu
          mode="inline"
          selectedKeys={[page]}
          onClick={(e) => setPage(e.key)}
          style={{
            background: 'transparent',
            border: 'none',
          }}
          items={[
            {
              key: 'detection',
              icon: <BgColorsOutlined />,
              label: 'Detection',
            },
            {
              key: 'about',
              icon: <InfoCircleOutlined />,
              label: 'About',
            },
            {
              key: 'help',
              icon: <QuestionCircleOutlined />,
              label: 'Help',
            },
          ]}
        />

        <div style={{ padding: '2rem 1.5rem', marginTop: '2rem', borderTop: '1px solid #2A3B52' }}>
          <h4 style={{ color: '#FFFFFF', marginBottom: '1rem' }}>Quick Stats</h4>
          <div className="metric-card">
            <div style={{ color: '#00D9A3', fontSize: '1.5rem', fontWeight: '700' }}>0</div>
            <div style={{ color: '#B4B8BE', fontSize: '0.875rem', marginTop: '0.5rem' }}>
              Analyses Today
            </div>
          </div>
          <div className="metric-card" style={{ marginTop: '1rem' }}>
            <div style={{ color: '#00D9A3', fontSize: '1.5rem', fontWeight: '700' }}>0%</div>
            <div style={{ color: '#B4B8BE', fontSize: '0.875rem', marginTop: '0.5rem' }}>
              Accuracy Rate
            </div>
          </div>
        </div>
      </Sider>

      <Layout>
        <Content style={{ padding: '0' }}>
          <div className="page-container">{renderPage()}</div>
        </Content>
      </Layout>
    </Layout>
  )
}
