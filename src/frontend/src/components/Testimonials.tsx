import { Star } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

const testimonials = [
    {
        name: "Sarah Jenkins",
        role: "Organic Farmer",
        content: "AgriGuard saved my tomato crop from early blight. The detection was spot on and the advice was incredibly helpful.",
        avatar: "SJ",
    },
    {
        name: "Michael Chen",
        role: "Agricultural Consultant",
        content: "A game-changer for quick field diagnosis. I use it daily to help my clients identify issues before they spread.",
        avatar: "MC",
    },
    {
        name: "David Ross",
        role: "Home Gardener",
        content: "I'm new to gardening and this app has been like having an expert in my pocket. Highly recommended!",
        avatar: "DR",
    },
];

const Testimonials = () => {
    return (
        <section className="py-20 bg-muted/30">
            <div className="container mx-auto px-4">
                <div className="text-center max-w-3xl mx-auto mb-16">
                    <h2 className="text-3xl md:text-4xl font-bold mb-4 text-foreground">
                        Trusted by Growers
                    </h2>
                    <p className="text-lg text-muted-foreground">
                        See what farmers and gardeners are saying about AgriGuard.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {testimonials.map((testimonial, index) => (
                        <Card key={index} className="border-none shadow-md bg-background/60 backdrop-blur-sm">
                            <CardContent className="pt-6">
                                <div className="flex gap-1 mb-4">
                                    {[...Array(5)].map((_, i) => (
                                        <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                                    ))}
                                </div>
                                <p className="text-muted-foreground mb-6 italic">
                                    "{testimonial.content}"
                                </p>
                                <div className="flex items-center gap-4">
                                    <Avatar>
                                        <AvatarImage src={`https://api.dicebear.com/7.x/initials/svg?seed=${testimonial.avatar}`} />
                                        <AvatarFallback>{testimonial.avatar}</AvatarFallback>
                                    </Avatar>
                                    <div>
                                        <p className="font-semibold text-sm">{testimonial.name}</p>
                                        <p className="text-xs text-muted-foreground">{testimonial.role}</p>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default Testimonials;
