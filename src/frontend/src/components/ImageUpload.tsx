import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { Upload, Loader2, Image as ImageIcon, Leaf } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";
import { api } from "@/lib/api";
import { AnalysisResult } from "@/types/analysis";

interface ImageUploadProps {
  onAnalysisStart: () => void;
  onAnalysisComplete: (result: AnalysisResult) => void;
  isAnalyzing: boolean;
}

const ImageUpload = ({ onAnalysisStart, onAnalysisComplete, isAnalyzing }: ImageUploadProps) => {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const { toast } = useToast();
  const navigate = useNavigate();

  const convertToBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = error => reject(error);
    });
  };

  const handleImageSelect = useCallback(async (file: File) => {
    if (!file.type.startsWith('image/')) {
      toast({
        title: "Invalid file type",
        description: "Please upload an image file (JPG, PNG, etc.)",
        variant: "destructive",
      });
      return;
    }

    try {
      const base64Image = await convertToBase64(file);
      setSelectedImage(base64Image);
      setFile(file);
      toast({
        title: "Image uploaded",
        description: "Click 'Analyze Plant' to start the disease detection",
      });
    } catch (error) {
      console.error('Error reading file:', error);
      toast({
        title: "Upload failed",
        description: "Failed to read the image file",
        variant: "destructive",
      });
    }
  }, [toast]);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleImageSelect(e.dataTransfer.files[0]);
    }
  }, [handleImageSelect]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleImageSelect(e.target.files[0]);
    }
  }, [handleImageSelect]);

  const analyzeImage = async () => {
    if (!selectedImage) {
      toast({
        title: "No image selected",
        description: "Please upload an image first",
        variant: "destructive",
      });
      return;
    }

    if (!api.isAuthenticated()) {
      toast({
        title: "Authentication required",
        description: "Please login to analyze images",
        variant: "destructive",
      });
      navigate("/login");
      return;
    }

    onAnalysisStart();

    try {
      if (!file) {
        throw new Error("File object missing. Please re-upload.");
      }

      const data = await api.analyze(file);

      toast({
        title: "Analysis complete",
        description: `Plant status: ${data.disease_name}`,
      });

      onAnalysisComplete({
        status: data.disease_name.toLowerCase().includes('healthy') ? 'healthy' : 'diseased',
        disease: data.disease_name,
        confidence: data.confidence,
        analysis: data.recommendation,
        recommendations: [data.recommendation],
        timestamp: data.timestamp
      });
    } catch (error) {
      console.error('Analysis error:', error);
      toast({
        title: "Analysis failed",
        description: error instanceof Error ? error.message : "Failed to analyze the image. Please try again.",
        variant: "destructive",
      });
      onAnalysisComplete({
        status: 'healthy',
        disease: 'none',
        confidence: 0,
        analysis: '',
        recommendations: [],
        timestamp: ''
      });
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-8">
      <Card className="p-8">
        <div
          className={`relative border-2 border-dashed rounded-lg p-12 text-center transition-colors ${dragActive ? 'border-primary bg-accent' : 'border-border hover:border-primary/50'
            }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            accept="image/*"
            onChange={handleFileInput}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            disabled={isAnalyzing}
          />

          {selectedImage ? (
            <div className="space-y-4">
              <img
                src={selectedImage}
                alt="Selected plant"
                className="max-h-64 mx-auto rounded-lg shadow-lg"
              />
              <p className="text-sm text-muted-foreground">
                Image ready for analysis
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="w-16 h-16 mx-auto rounded-full bg-accent flex items-center justify-center">
                <ImageIcon className="w-8 h-8 text-primary" />
              </div>
              <div>
                <p className="text-lg font-semibold text-foreground mb-2">
                  Drop your plant image here
                </p>
                <p className="text-sm text-muted-foreground">
                  or click to browse files
                </p>
              </div>
              <Upload className="w-8 h-8 mx-auto text-muted-foreground" />
            </div>
          )}
        </div>

        {selectedImage && (
          <div className="flex gap-3 mt-6">
            <Button
              onClick={analyzeImage}
              disabled={isAnalyzing}
              className="flex-1"
              size="lg"
            >
              {isAnalyzing ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Leaf className="mr-2 h-5 w-5" />
                  Analyze Plant
                </>
              )}
            </Button>

            <Button
              variant="outline"
              onClick={() => setSelectedImage(null)}
              disabled={isAnalyzing}
              size="lg"
            >
              Clear
            </Button>
          </div>
        )}
      </Card>

      <div className="text-center space-y-2">
        <h3 className="text-xl font-semibold text-foreground">How it works</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
          <Card className="p-4">
            <div className="w-10 h-10 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold mb-3 mx-auto">
              1
            </div>
            <h4 className="font-semibold mb-2">Upload Image</h4>
            <p className="text-sm text-muted-foreground">
              Take a clear photo of the plant leaf
            </p>
          </Card>

          <Card className="p-4">
            <div className="w-10 h-10 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold mb-3 mx-auto">
              2
            </div>
            <h4 className="font-semibold mb-2">AI Analysis</h4>
            <p className="text-sm text-muted-foreground">
              Our AI analyzes for diseases instantly
            </p>
          </Card>

          <Card className="p-4">
            <div className="w-10 h-10 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold mb-3 mx-auto">
              3
            </div>
            <h4 className="font-semibold mb-2">Get Results</h4>
            <p className="text-sm text-muted-foreground">
              Receive diagnosis and treatment advice
            </p>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default ImageUpload;
