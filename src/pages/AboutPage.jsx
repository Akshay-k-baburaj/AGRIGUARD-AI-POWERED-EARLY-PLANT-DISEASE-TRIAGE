import React from 'react'
import { Card, Row, Col, List } from 'antd'
import { CheckCircleOutlined, ThunderboltOutlined } from '@ant-design/icons'

export default function AboutPage() {
  const features = [
    {
      title: 'Image Classification',
      description: 'Analyze leaf photos to detect diseases',
      icon: '📷',
    },
    {
      title: 'Health Status',
      description: 'Determine if crops are Healthy or Diseased',
      icon: '🌱',
    },
    {
      title: 'Recommendations',
      description: 'Receive actionable agricultural advice',
      icon: '💡',
    },
    {
      title: 'Mobile Ready',
      description: 'Optimized for deployment on edge devices',
      icon: '📱',
    },
  ]

  return (
    <div>
      <h1>About AgriGuard</h1>

      <Card
        style={{
          background: 'linear-gradient(135deg, #131B2E 0%, #1A2537 100%)',
          border: '1px solid #2A3B52',
          borderRadius: '12px',
          marginBottom: '2rem',
        }}
      >
        <p style={{ fontSize: '1.1rem', color: '#B4B8BE', marginBottom: '1.5rem' }}>
          AgriGuard is an AI-powered plant disease detection system designed to help farmers and
          agricultural professionals identify plant diseases early and take preventive action.
        </p>
      </Card>

      <h2 style={{ marginBottom: '1.5rem' }}>Features</h2>
      <Row gutter={[16, 16]} style={{ marginBottom: '2rem' }}>
        {features.map((feature, index) => (
          <Col xs={24} sm={12} md={12} key={index}>
            <Card
              style={{
                background: 'linear-gradient(135deg, #131B2E 0%, #1A2537 100%)',
                border: '1px solid #2A3B52',
                borderRadius: '12px',
                height: '100%',
              }}
            >
              <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>{feature.icon}</div>
              <h3 style={{ marginBottom: '0.5rem' }}>{feature.title}</h3>
              <p style={{ color: '#B4B8BE', marginBottom: 0 }}>{feature.description}</p>
            </Card>
          </Col>
        ))}
      </Row>

      <h2 style={{ marginBottom: '1.5rem' }}>Technology</h2>
      <Card
        style={{
          background: 'linear-gradient(135deg, #131B2E 0%, #1A2537 100%)',
          border: '1px solid #2A3B52',
          borderRadius: '12px',
        }}
      >
        <p style={{ fontSize: '1.1rem', color: '#B4B8BE' }}>
          Built with deep learning and computer vision to provide accurate, real-time disease
          detection suitable for field use.
        </p>
      </Card>
    </div>
  )
}
