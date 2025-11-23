export interface AnalysisResult {
  status: 'healthy' | 'diseased';
  disease: string;
  confidence: number;
  analysis: string;
  recommendations: string[];
  timestamp: string;
  image_hash?: string;
}
