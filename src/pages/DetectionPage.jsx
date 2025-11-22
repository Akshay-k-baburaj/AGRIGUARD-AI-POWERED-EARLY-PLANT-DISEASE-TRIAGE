import React, { useState } from 'react'
import { Card, Row, Col, Button, Upload, Spin, message, Statistic } from 'antd'
import { UploadOutlined } from '@ant-design/icons'

export default function DetectionPage() {
  const [uploaded, setUploaded] = useState(false)
  const [loading, setLoading] = useState(false)
  const [analyzed, setAnalyzed] = useState(false)
  const [imageUrl, setImageUrl] = useState(null)

  const handleUpload = (file) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      setImageUrl(e.target.result)
      setUploaded(true)
      setAnalyzed(false)
    }
    reader.readAsDataURL(file)
    return false
  }

  const handleAnalyze = () => {
    setLoading(true)
    setTimeout(() => {
      setLoading(false)
      setAnalyzed(true)
      message.success('Analysis complete!')
    }, 2000)
  }

  return (
    <div>
      <h1>Plant Disease Detection</h1>
      <p style={{ marginBottom: '2rem' }}>
        Upload a leaf image to analyze its health status and receive agricultural recommendations.
      </p>

      <Row gutter={[24, 24]}>
        <Col xs={24} sm={24} md={12}>
          <Card
            style={{
              background: 'linear-gradient(135deg, #131B2E 0%, #1A2537 100%)',
              border: '1px solid #2A3B52',
              borderRadius: '12px',
            }}
            title={<h3 style={{ marginBottom: 0 }}>Upload Image</h3>}
          >
            <Upload.Dragger
              accept="image/jpeg,image/png,.jpg,.jpeg,.png"
              beforeUpload={handleUpload}
              showUploadList={false}
              style={{
                background: 'transparent',
                border: '2px dashed #2A3B52',
                borderRadius: '8px',
                padding: '2rem',
              }}
            >
              <p style={{ color: '#B4B8BE', fontSize: '1rem' }}>
                <UploadOutlined style={{ fontSize: '2rem', color: '#00D9A3', marginBottom: '1rem' }} />
              </p>
              <p style={{ color: '#E8EAED', fontSize: '1rem' }}>
                Click or drag a leaf image here
              </p>
              <p style={{ color: '#B4B8BE', fontSize: '0.875rem' }}>
                Support for JPG, JPEG, PNG
              </p>
            </Upload.Dragger>

            {imageUrl && (
              <div style={{ marginTop: '1.5rem' }}>
                <img
                  src={imageUrl}
                  alt="Uploaded"
                  style={{
                    width: '100%',
                    borderRadius: '8px',
                    border: '1px solid #2A3B52',
                  }}
                />
                <Button
                  type="primary"
                  size="large"
                  loading={loading}
                  onClick={handleAnalyze}
                  block
                  style={{
                    marginTop: '1rem',
                    background: '#00D9A3',
                    color: '#0A0F1E',
                    border: 'none',
                    fontWeight: '600',
                  }}
                >
                  {loading ? 'Analyzing...' : 'Analyze Image'}
                </Button>
              </div>
            )}
          </Card>
        </Col>

        <Col xs={24} sm={24} md={12}>
          <Card
            style={{
              background: 'linear-gradient(135deg, #131B2E 0%, #1A2537 100%)',
              border: '1px solid #2A3B52',
              borderRadius: '12px',
            }}
            title={<h3 style={{ marginBottom: 0 }}>Results</h3>}
          >
            {!uploaded ? (
              <div
                style={{
                  padding: '2rem',
                  background: 'rgba(33, 150, 243, 0.1)',
                  border: '1px solid rgba(33, 150, 243, 0.3)',
                  borderRadius: '8px',
                  color: '#B4B8BE',
                }}
              >
                Please upload an image to begin analysis.
              </div>
            ) : !analyzed ? (
              <div
                style={{
                  padding: '2rem',
                  background: 'rgba(33, 150, 243, 0.1)',
                  border: '1px solid rgba(33, 150, 243, 0.3)',
                  borderRadius: '8px',
                  color: '#B4B8BE',
                }}
              >
                Upload an image and click 'Analyze Image' to see results here.
              </div>
            ) : (
              <div style={{ color: '#E8EAED' }}>
                <p style={{ marginBottom: '1rem' }}>Analysis results will appear here.</p>
              </div>
            )}

            <div style={{ marginTop: '2rem', borderTop: '1px solid #2A3B52', paddingTop: '2rem' }}>
              <h3 style={{ marginBottom: '1.5rem' }}>Sample Predictions</h3>
              <Row gutter={[16, 16]}>
                <Col xs={12}>
                  <Card
                    style={{
                      background: 'transparent',
                      border: '1px solid #2A3B52',
                      textAlign: 'center',
                      padding: '1rem',
                    }}
                  >
                    <Statistic
                      title="Confidence"
                      value="0"
                      suffix="%"
                      valueStyle={{ color: '#00D9A3' }}
                    />
                  </Card>
                </Col>
                <Col xs={12}>
                  <Card
                    style={{
                      background: 'transparent',
                      border: '1px solid #2A3B52',
                      textAlign: 'center',
                      padding: '1rem',
                    }}
                  >
                    <Statistic
                      title="Status"
                      value="Pending"
                      valueStyle={{ color: '#00D9A3', fontSize: '1.5rem' }}
                    />
                  </Card>
                </Col>
              </Row>
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  )
}
