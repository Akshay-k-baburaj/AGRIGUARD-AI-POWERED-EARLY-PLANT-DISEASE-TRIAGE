import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Header from "@/components/Header";
import ImageUpload from "@/components/ImageUpload";
import ResultsDisplay from "@/components/ResultsDisplay";
import ScanHistory from "@/components/ScanHistory";
import { AnalysisResult } from "@/types/analysis";
import { api } from "@/lib/api";

const Dashboard = () => {
    const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [refreshTrigger, setRefreshTrigger] = useState(0);
    const navigate = useNavigate();

    useEffect(() => {
        if (!api.isAuthenticated()) {
            navigate("/login");
        }
    }, [navigate]);

    const handleAnalysisComplete = (result: AnalysisResult) => {
        setAnalysisResult(result);
        setIsAnalyzing(false);
        setRefreshTrigger(prev => prev + 1);
    };

    const handleReset = () => {
        setAnalysisResult(null);
        setIsAnalyzing(false);
    };

    return (
        <div className="min-h-screen bg-background flex flex-col">
            <Header />

            <main className="container mx-auto px-4 py-24 flex-grow">
                <div className="max-w-4xl mx-auto space-y-12">
                    <div>
                        <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
                        <p className="text-muted-foreground">Manage your crops and analyze plant health.</p>
                    </div>

                    <section className="bg-muted/30 p-8 rounded-xl border border-border/50">
                        <div className="mb-8">
                            <h2 className="text-xl font-semibold mb-2">New Analysis</h2>
                            <p className="text-sm text-muted-foreground">Upload an image to detect diseases.</p>
                        </div>

                        {!analysisResult ? (
                            <ImageUpload
                                onAnalysisStart={() => setIsAnalyzing(true)}
                                onAnalysisComplete={handleAnalysisComplete}
                                isAnalyzing={isAnalyzing}
                            />
                        ) : (
                            <ResultsDisplay
                                result={analysisResult}
                                onReset={handleReset}
                            />
                        )}
                    </section>

                    <section>
                        <ScanHistory
                            refreshTrigger={refreshTrigger}
                            onError={(error) => {
                                if (error.message.includes("401") || error.message.includes("authenticated")) {
                                    api.logout();
                                    navigate("/login");
                                }
                            }}
                        />
                    </section>
                </div>
            </main>
        </div>
    );
};

export default Dashboard;
