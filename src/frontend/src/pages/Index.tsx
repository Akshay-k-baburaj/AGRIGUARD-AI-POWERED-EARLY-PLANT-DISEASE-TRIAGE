import Hero from "@/components/Hero";
import Header from "@/components/Header";
import Features from "@/components/Features";
import HowItWorks from "@/components/HowItWorks";
import Footer from "@/components/Footer";

const Index = () => {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header />
      <Hero />

      <Features />
      <HowItWorks />

      <Footer />
    </div>
  );
};

export default Index;
