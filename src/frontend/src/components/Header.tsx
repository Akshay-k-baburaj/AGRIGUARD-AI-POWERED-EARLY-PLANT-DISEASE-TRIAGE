import { Leaf } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";

const Header = () => {
    const navigate = useNavigate();
    const isAuthenticated = api.isAuthenticated();

    const handleLogout = () => {
        api.logout();
        navigate("/");
    };

    return (
        <header className="fixed top-0 left-0 right-0 z-50 border-b border-border/40 bg-background/80 backdrop-blur-md supports-[backdrop-filter]:bg-background/60">
            <div className="container mx-auto px-4 h-16 flex items-center justify-between">
                <Link to={isAuthenticated ? "/dashboard" : "/"} className="flex items-center gap-2 hover:opacity-90 transition-opacity">
                    <div className="bg-primary/10 p-2 rounded-full">
                        <Leaf className="w-6 h-6 text-primary" />
                    </div>
                    <span className="text-xl font-bold text-foreground tracking-tight">
                        AgriGuard
                    </span>
                </Link>

                <div className="flex items-center gap-4">
                    {isAuthenticated ? (
                        <>
                            <Link to="/dashboard">
                                <Button variant="ghost" className="text-muted-foreground hover:text-foreground">
                                    Dashboard
                                </Button>
                            </Link>
                            <Button
                                variant="outline"
                                onClick={handleLogout}
                            >
                                Logout
                            </Button>
                        </>
                    ) : (
                        <>
                            <Link to="/login">
                                <Button variant="ghost" className="text-muted-foreground hover:text-foreground">
                                    Login
                                </Button>
                            </Link>
                            <Link to="/register">
                                <Button className="bg-primary hover:bg-primary/90 text-primary-foreground shadow-sm">
                                    Get Started
                                </Button>
                            </Link>
                        </>
                    )}
                </div>
            </div>
        </header>
    );
};

export default Header;
