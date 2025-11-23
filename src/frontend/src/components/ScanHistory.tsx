import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { AnalysisResult } from "@/types/analysis";
import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from "@/components/ui/accordion";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Loader2 } from "lucide-react";

interface ScanHistoryProps {
    refreshTrigger?: number;
}

const ScanHistory = ({ refreshTrigger = 0 }: ScanHistoryProps) => {
    const [history, setHistory] = useState<AnalysisResult[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const checkAuthAndFetch = async () => {
            const auth = api.isAuthenticated();
            setIsAuthenticated(auth);

            if (auth) {
                try {
                    const data = await api.getHistory();
                    // Map backend response to AnalysisResult if needed, or ensure backend returns compatible format
                    // Backend returns list of schemas.ScanOut which has: id, image_hash, disease_name, confidence, recommendation, timestamp
                    // AnalysisResult expects: status, disease, confidence, analysis, recommendations, timestamp, image_hash

                    const mappedHistory = data.map((scan: any) => ({
                        status: scan.disease_name.toLowerCase().includes('healthy') ? 'healthy' : 'diseased',
                        disease: scan.disease_name,
                        confidence: scan.confidence,
                        analysis: scan.recommendation, // Mapping recommendation to analysis
                        recommendations: [scan.recommendation], // Wrapping in array
                        timestamp: scan.timestamp,
                        image_hash: scan.image_hash
                    }));

                    setHistory(mappedHistory);
                } catch (error) {
                    console.error("Failed to fetch history", error);
                } finally {
                    setIsLoading(false);
                }
            } else {
                setIsLoading(false);
            }
        };

        checkAuthAndFetch();
    }, [refreshTrigger]);

    if (!isAuthenticated) {
        return null;
    }

    if (isLoading) {
        return (
            <div className="flex justify-center p-8">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
        );
    }

    if (history.length === 0) {
        return (
            <Card className="mt-8">
                <CardHeader>
                    <CardTitle>Recent Scans</CardTitle>
                    <p className="text-muted-foreground">No scan history found.</p>
                </CardHeader>
            </Card>
        );
    }

    return (
        <Card className="mt-8 border-none shadow-md bg-white/50 backdrop-blur-sm">
            <CardHeader className="border-b bg-muted/20 pb-4">
                <CardTitle className="text-xl font-semibold text-primary flex items-center gap-2">
                    Recent Scans
                </CardTitle>
            </CardHeader>
            <div className="p-0">
                <Accordion type="single" collapsible className="w-full">
                    {history.map((scan, index) => (
                        <AccordionItem key={index} value={`item-${index}`} className="border-b last:border-0 px-6 py-2 hover:bg-muted/10 transition-colors">
                            <AccordionTrigger className="hover:no-underline py-4">
                                <div className="flex items-center justify-between w-full pr-4">
                                    <div className="flex items-center gap-4">
                                        <div className={`w-2 h-2 rounded-full ${scan.status === 'healthy' ? 'bg-green-500' : 'bg-red-500'}`} />
                                        <div className="flex flex-col items-start gap-1">
                                            <span className="font-medium text-base text-foreground">
                                                {scan.disease.split('___').map(part => part.split('_').join(' ')).join(' - ')}
                                            </span>
                                            <span className="text-xs text-muted-foreground">
                                                {new Date(scan.timestamp).toLocaleDateString(undefined, {
                                                    year: 'numeric',
                                                    month: 'short',
                                                    day: 'numeric',
                                                    hour: '2-digit',
                                                    minute: '2-digit'
                                                })}
                                            </span>
                                        </div>
                                    </div>
                                    <Badge
                                        variant={scan.status === 'healthy' ? "outline" : "destructive"}
                                        className={`${scan.status === 'healthy' ? 'border-green-500 text-green-700 bg-green-50' : ''} shadow-sm`}
                                    >
                                        {scan.status === 'healthy' ? 'Healthy' : 'Detected'}
                                    </Badge>
                                </div>
                            </AccordionTrigger>
                            <AccordionContent>
                                <div className="pl-6 pr-4 pb-4 space-y-4">
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="bg-muted/30 p-3 rounded-lg">
                                            <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Confidence</span>
                                            <p className="text-lg font-semibold text-primary mt-1">
                                                {(scan.confidence * 100).toFixed(1)}%
                                            </p>
                                        </div>
                                        <div className="bg-muted/30 p-3 rounded-lg">
                                            <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Status</span>
                                            <p className="text-lg font-semibold mt-1 capitalize">
                                                {scan.status}
                                            </p>
                                        </div>
                                    </div>

                                    <div className="bg-blue-50/50 border border-blue-100 p-4 rounded-lg">
                                        <span className="text-xs font-medium text-blue-600 uppercase tracking-wider mb-2 block">Recommendation</span>
                                        <p className="text-sm text-foreground/80 leading-relaxed">
                                            {scan.analysis}
                                        </p>
                                    </div>
                                </div>
                            </AccordionContent>
                        </AccordionItem>
                    ))}
                </Accordion>
            </div>
        </Card>
    );
};

export default ScanHistory;
