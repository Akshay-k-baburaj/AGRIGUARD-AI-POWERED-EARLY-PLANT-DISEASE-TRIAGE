import { Shield, Zap, Sprout, Lock } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const features = [
    {
        title: "AI-Powered Analysis",
        description: "Advanced machine learning algorithms detect plant diseases with high accuracy.",
        icon: Zap,
    },
    {
        title: "Instant Results",
        description: "Get immediate diagnosis and actionable insights within seconds of uploading.",
        icon: Sprout,
    },
    {
        title: "Expert Recommendations",
        description: "Receive tailored treatment plans and preventative measures for your crops.",
        icon: Shield,
    },
    {
        title: "Secure History",
        description: "Your scan history is securely stored and easily accessible for future reference.",
        icon: Lock,
    },
];

const Features = () => {
    return (
        <section className="py-20 bg-muted/30">
            <div className="container mx-auto px-4">
                <div className="text-center max-w-3xl mx-auto mb-16">
                    <h2 className="text-3xl md:text-4xl font-bold mb-4 text-foreground">
                        Why Choose AgriGuard?
                    </h2>
                    <p className="text-lg text-muted-foreground">
                        We combine cutting-edge technology with agricultural expertise to help you protect your harvest.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                    {features.map((feature, index) => (
                        <Card key={index} className="border-none shadow-lg bg-background/60 backdrop-blur-sm hover:translate-y-[-5px] transition-transform duration-300">
                            <CardHeader className="space-y-4">
                                <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                                    <feature.icon className="w-6 h-6 text-primary" />
                                </div>
                                <CardTitle className="text-xl">{feature.title}</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p className="text-muted-foreground leading-relaxed">
                                    {feature.description}
                                </p>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default Features;
