import { Leaf } from "lucide-react";
import { Link } from "react-router-dom";

const Footer = () => {
    return (
        <footer className="bg-background border-t border-border pt-16 pb-8">
            <div className="container mx-auto px-4">
                <div className="flex flex-col items-center text-center mb-12">
                    <Link to="/" className="flex items-center gap-2 mb-4">
                        <Leaf className="w-6 h-6 text-primary" />
                        <span className="text-xl font-bold text-foreground">AgriGuard</span>
                    </Link>
                    <p className="text-muted-foreground text-sm leading-relaxed max-w-md">
                        Empowering farmers with AI-driven plant disease detection for healthier crops and better yields.
                    </p>
                </div>

                <div className="border-t border-border pt-8 text-center text-sm text-muted-foreground">
                    <p>© {new Date().getFullYear()} AgriGuard. All rights reserved.</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
