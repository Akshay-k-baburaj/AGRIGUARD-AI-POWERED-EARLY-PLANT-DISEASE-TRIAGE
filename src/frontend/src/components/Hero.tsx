const Hero = () => {
  return (

    <div className="relative pt-32 pb-20 overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 -z-10 bg-[linear-gradient(to_right,#8080800a_1px,transparent_1px),linear-gradient(to_bottom,#8080800a_1px,transparent_1px)] bg-[size:14px_24px]"></div>
      <div className="absolute left-0 right-0 top-0 -z-10 m-auto h-[310px] w-[310px] rounded-full bg-primary/20 opacity-20 blur-[100px]"></div>

      <div className="container mx-auto px-4">

        <div className="max-w-4xl mx-auto text-center space-y-6">
          <h2 className="text-3xl md:text-5xl font-bold text-foreground leading-tight">
            AI-Powered
            <br />
            <span className="text-primary">Plant Disease Detection</span>
          </h2>

          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto">
            Upload a leaf image and get instant AI-powered disease analysis with
            actionable agricultural recommendations to protect your crops
          </p>

          <div className="flex items-center justify-center gap-8 pt-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">AI</div>
              <div className="text-sm text-muted-foreground">Powered</div>
            </div>
            <div className="w-px h-12 bg-border"></div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">Instant</div>
              <div className="text-sm text-muted-foreground">Analysis</div>
            </div>
            <div className="w-px h-12 bg-border"></div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">Expert</div>
              <div className="text-sm text-muted-foreground">Advice</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;
