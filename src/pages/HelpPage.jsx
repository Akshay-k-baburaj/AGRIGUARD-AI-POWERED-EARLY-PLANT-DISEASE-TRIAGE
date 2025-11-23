import React from 'react'
import { Collapse, Card } from 'antd'
import { CameraOutlined, SearchOutlined, BulbOutlined } from '@ant-design/icons'

export default function HelpPage() {
  const items = [
    {
      key: '1',
      label: (
        <span>
          <CameraOutlined style={{ marginRight: '0.5rem', color: '#00D9A3' }} />
          Taking Photos
        </span>
      ),
      children: (
        <div style={{ color: '#B4B8BE' }}>
          <ul>
            <li>Take clear, well-lit photos of leaves</li>
            <li>Ensure the leaf fills most of the frame</li>
            <li>Avoid blurry or dark images</li>
            <li>Capture both sides if possible</li>
          </ul>
        </div>
      ),
    },
    {
      key: '2',
      label: (
        <span>
          <SearchOutlined style={{ marginRight: '0.5rem', color: '#00D9A3' }} />
          Getting Results
        </span>
      ),
      children: (
        <div style={{ color: '#B4B8BE' }}>
          <ul>
            <li>Upload your image using the file uploader</li>
            <li>Click the 'Analyze Image' button</li>
            <li>View the disease classification and confidence score</li>
            <li>Read the agricultural recommendations</li>
          </ul>
        </div>
      ),
    },
    {
      key: '3',
      label: (
        <span>
          <BulbOutlined style={{ marginRight: '0.5rem', color: '#00D9A3' }} />
          Best Practices
        </span>
      ),
      children: (
        <div style={{ color: '#B4B8BE' }}>
          <ul>
            <li>Use images taken in natural lighting</li>
            <li>Ensure leaves are dry and clearly visible</li>
            <li>Include any visible symptoms in the frame</li>
            <li>Regular monitoring provides best results</li>
          </ul>
        </div>
      ),
    },
  ]

  return (
    <div>
      <h1>How to Use AgriGuard</h1>
      <p style={{ marginBottom: '2rem', color: '#B4B8BE' }}>
        Follow these guidelines to get the best results from AgriGuard's plant disease detection
        system.
      </p>

      <Collapse
        items={items}
        defaultActiveKey={['1']}
        style={{
          background: 'transparent',
          border: '1px solid #2A3B52',
          borderRadius: '12px',
        }}
      />
    </div>
  )
}
