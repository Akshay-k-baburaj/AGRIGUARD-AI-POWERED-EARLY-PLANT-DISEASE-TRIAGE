import { Upload, Search, FileCheck } from "lucide-react";

const steps = [
    {
        title: "Upload Image",
        description: "Take a photo of the affected plant leaf or upload an existing image.",
        icon: Upload,
    },
    {
        title: "AI Analysis",
        description: "Our advanced AI scans the image to identify disease patterns and symptoms.",
        icon: Search,
    },
    {
        title: "Get Results",
        description: "Receive instant diagnosis and detailed treatment recommendations.",
        icon: FileCheck,
    },
];

const HowItWorks = () => {
    return (
        <section className="py-20 bg-background">
            <div className="container mx-auto px-4">
                <div className="text-center max-w-3xl mx-auto mb-16">
                    <h2 className="text-3xl md:text-4xl font-bold mb-4 text-foreground">
                        How It Works
                    </h2>
                    <p className="text-lg text-muted-foreground">
                        Diagnose plant diseases in three simple steps.
                    </p>
                </div>

                <div className="relative grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
                    {/* Connecting Line (Desktop only) */}
                    <div className="hidden md:block absolute top-12 left-[16%] right-[16%] h-0.5 bg-gradient-to-r from-primary/20 via-primary/50 to-primary/20 -z-10" />

                    {steps.map((step, index) => (
                        <div key={index} className="flex flex-col items-center text-center group">
                            <div className="w-24 h-24 rounded-full bg-background border-4 border-muted group-hover:border-primary/50 transition-colors flex items-center justify-center mb-6 shadow-lg relative z-10">
                                <step.icon className="w-10 h-10 text-primary" />
                            </div>
                            <h3 className="text-xl font-semibold mb-3">{step.title}</h3>
                            <p className="text-muted-foreground max-w-xs mx-auto">
                                {step.description}
                            </p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default HowItWorks;
