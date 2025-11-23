import { AlertCircle, CheckCircle, RefreshCw, Calendar } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { AnalysisResult } from "@/types/analysis";

interface ResultsDisplayProps {
  result: AnalysisResult;
  onReset: () => void;
}

const ResultsDisplay = ({ result, onReset }: ResultsDisplayProps) => {
  const isHealthy = result.status === 'healthy';
  const StatusIcon = isHealthy ? CheckCircle : AlertCircle;
  const statusColor = isHealthy ? 'text-primary' : 'text-destructive';
  const statusBgColor = isHealthy ? 'bg-primary/10' : 'bg-destructive/10';

  const formatDate = (timestamp: string) => {
    return new Date(timestamp).toLocaleString('en-US', {
      dateStyle: 'medium',
      timeStyle: 'short'
    });
  };

  const formatDiseaseName = (name: string) => {
    return name.split('___').map(part => part.split('_').join(' ')).join(' - ');
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-in fade-in-50 duration-500">
      <Card className="p-8">
        <div className="flex items-start justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className={`w-16 h-16 rounded-full ${statusBgColor} flex items-center justify-center`}>
              <StatusIcon className={`w-8 h-8 ${statusColor}`} />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-foreground">
                Analysis Results
              </h2>
              <div className="flex flex-col gap-1 mt-1 text-sm text-muted-foreground">
                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  <span>{formatDate(result.timestamp)}</span>
                </div>
                {result.image_hash && (
                  <div className="text-xs font-mono">
                    Hash: {result.image_hash.substring(0, 10)}...
                  </div>
                )}
              </div>
            </div>
          </div>
          <Button variant="outline" onClick={onReset}>
            <RefreshCw className="w-4 h-4 mr-2" />
            New Analysis
          </Button>
        </div>

        <div className="space-y-6">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-foreground">Plant Status</span>
              <Badge variant={isHealthy ? "default" : "destructive"} className="uppercase">
                {result.status}
              </Badge>
            </div>

            {!isHealthy && result.disease !== 'none' && (
              <div className="bg-destructive/5 border border-destructive/20 rounded-lg p-4">
                <span className="text-xs font-bold text-destructive uppercase tracking-wider block mb-1">
                  Detected Disease
                </span>
                <span className="text-lg font-bold text-foreground">
                  {formatDiseaseName(result.disease)}
                </span>
              </div>
            )}

            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-foreground">Confidence Score</span>
                <span className="text-sm font-semibold text-foreground">
                  {(result.confidence * 100).toFixed(2)}%
                </span>
              </div>
              <Progress value={result.confidence * 100} className="h-2" />
            </div>
          </div>

          {result.analysis && (
            <Card className="p-4 bg-accent">
              <h3 className="font-semibold text-foreground mb-2">Analysis Details</h3>
              <p className="text-sm text-muted-foreground">{result.analysis}</p>
            </Card>
          )}
        </div>
      </Card>

      {result.recommendations && result.recommendations.length > 0 && (
        <Card className="p-8">
          <h3 className="text-xl font-bold text-foreground mb-4 flex items-center gap-2">
            <span className="w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-sm font-bold">
              ✓
            </span>
            Recommended Actions
          </h3>
          <ul className="space-y-3">
            {result.recommendations.map((recommendation, index) => (
              <li
                key={index}
                className="flex items-start gap-3 p-3 rounded-lg hover:bg-accent transition-colors"
              >
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-primary/20 text-primary flex items-center justify-center text-xs font-bold mt-0.5">
                  {index + 1}
                </span>
                <p className="text-sm text-foreground flex-1">{recommendation}</p>
              </li>
            ))}
          </ul>
        </Card>
      )}

      <Card className="p-6 bg-muted/50">
        <p className="text-sm text-muted-foreground text-center">
          <strong>Note:</strong> These recommendations are for informational purposes.
          For severe infestations or uncertain diagnoses, please consult with a local
          agricultural extension office or plant disease specialist.
        </p>
      </Card>
    </div>
  );
};

export default ResultsDisplay;
