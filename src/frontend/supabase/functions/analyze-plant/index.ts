// Edge function for plant disease analysis

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

interface DiseaseRecommendation {
  disease: string;
  recommendations: string[];
}

const diseaseRecommendations: Record<string, DiseaseRecommendation> = {
  "Bacterial Spot": {
    disease: "Bacterial Spot",
    recommendations: [
      "Remove and destroy infected leaves immediately",
      "Apply copper-based bactericides during cool, dry weather",
      "Improve air circulation by proper plant spacing",
      "Avoid overhead watering to reduce leaf wetness",
      "Rotate crops with non-susceptible plants"
    ]
  },
  "Early Blight": {
    disease: "Early Blight",
    recommendations: [
      "Remove lower infected leaves to prevent spread",
      "Apply organic fungicides like neem oil or copper spray",
      "Mulch around plants to prevent soil splash",
      "Ensure proper plant spacing for air circulation",
      "Water at the base of plants, avoid wetting foliage"
    ]
  },
  "Late Blight": {
    disease: "Late Blight",
    recommendations: [
      "Remove and destroy all infected plant material immediately",
      "Apply fungicides containing chlorothalonil or copper",
      "Improve drainage to reduce moisture",
      "Avoid working with plants when wet",
      "Consider resistant varieties for future planting"
    ]
  },
  "Leaf Mold": {
    disease: "Leaf Mold",
    recommendations: [
      "Increase ventilation in greenhouse or growing area",
      "Reduce humidity levels below 85%",
      "Remove infected leaves promptly",
      "Apply sulfur-based fungicides if needed",
      "Space plants properly for air circulation"
    ]
  },
  "Septoria Leaf Spot": {
    disease: "Septoria Leaf Spot",
    recommendations: [
      "Remove and destroy infected leaves",
      "Apply organic fungicides like copper spray",
      "Mulch to prevent soil-borne spore splash",
      "Rotate crops annually",
      "Water early in the day to allow foliage to dry"
    ]
  },
  "Spider Mites": {
    disease: "Spider Mites (Two-spotted)",
    recommendations: [
      "Spray plants with strong water stream to dislodge mites",
      "Apply neem oil or insecticidal soap",
      "Introduce beneficial predatory mites",
      "Increase humidity around plants",
      "Remove heavily infested leaves"
    ]
  },
  "Target Spot": {
    disease: "Target Spot",
    recommendations: [
      "Remove infected plant debris",
      "Apply copper-based fungicides",
      "Improve air circulation through pruning",
      "Avoid overhead irrigation",
      "Practice crop rotation"
    ]
  },
  "Yellow Leaf Curl Virus": {
    disease: "Yellow Leaf Curl Virus",
    recommendations: [
      "Remove and destroy infected plants immediately",
      "Control whitefly populations with insecticidal soap",
      "Use reflective mulches to deter whiteflies",
      "Plant virus-resistant varieties",
      "Remove weeds that can host the virus"
    ]
  },
  "Mosaic Virus": {
    disease: "Mosaic Virus",
    recommendations: [
      "Remove and destroy infected plants",
      "Control aphid populations that spread the virus",
      "Disinfect tools between plants",
      "Plant resistant varieties",
      "Remove weeds that can harbor the virus"
    ]
  },
  "Powdery Mildew": {
    disease: "Powdery Mildew",
    recommendations: [
      "Apply organic fungicides like sulfur or potassium bicarbonate",
      "Improve air circulation around plants",
      "Remove infected leaves",
      "Avoid overhead watering",
      "Plant in full sun locations when possible"
    ]
  }
};

function getRecommendations(detectedDisease: string): DiseaseRecommendation {
  // Try to find exact match first
  if (diseaseRecommendations[detectedDisease]) {
    return diseaseRecommendations[detectedDisease];
  }
  
  // Try to find partial match
  const lowerDisease = detectedDisease.toLowerCase();
  for (const [key, value] of Object.entries(diseaseRecommendations)) {
    if (lowerDisease.includes(key.toLowerCase()) || key.toLowerCase().includes(lowerDisease)) {
      return value;
    }
  }
  
  // Default recommendations for unknown diseases
  return {
    disease: detectedDisease,
    recommendations: [
      "Isolate affected plants to prevent spread",
      "Remove and destroy visibly infected plant parts",
      "Improve air circulation and reduce humidity",
      "Avoid overhead watering",
      "Consider consulting with a local agricultural extension office for specific treatment"
    ]
  };
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { image } = await req.json();
    
    if (!image) {
      throw new Error('No image provided');
    }

    const LOVABLE_API_KEY = Deno.env.get('LOVABLE_API_KEY');
    if (!LOVABLE_API_KEY) {
      throw new Error('LOVABLE_API_KEY not configured');
    }

    console.log('Analyzing plant image with AI...');

    const response = await fetch('https://ai.gateway.lovable.dev/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${LOVABLE_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'google/gemini-2.5-flash',
        messages: [
          {
            role: 'system',
            content: `You are an expert agricultural AI specialized in plant disease detection. 
            Analyze the plant leaf image and determine:
            1. Whether the plant is HEALTHY or DISEASED
            2. If diseased, identify the specific disease name
            3. Provide a confidence score (0-100)
            
            Respond ONLY with a JSON object in this exact format:
            {
              "status": "healthy" or "diseased",
              "disease": "disease name" or "none",
              "confidence": number between 0 and 100,
              "analysis": "brief description of what you observe"
            }
            
            Common plant diseases include: Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus, Powdery Mildew.`
          },
          {
            role: 'user',
            content: [
              {
                type: 'text',
                text: 'Please analyze this plant leaf image for diseases.'
              },
              {
                type: 'image_url',
                image_url: {
                  url: image
                }
              }
            ]
          }
        ],
      }),
    });

    if (!response.ok) {
      if (response.status === 429) {
        return new Response(
          JSON.stringify({ error: 'Rate limit exceeded. Please try again later.' }),
          { status: 429, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        );
      }
      if (response.status === 402) {
        return new Response(
          JSON.stringify({ error: 'AI service requires payment. Please contact support.' }),
          { status: 402, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        );
      }
      const errorText = await response.text();
      console.error('AI API error:', response.status, errorText);
      throw new Error(`AI API error: ${response.status}`);
    }

    const data = await response.json();
    console.log('AI response received:', data);

    const content = data.choices[0].message.content;
    
    // Extract JSON from the response (it might be wrapped in markdown code blocks)
    let analysisResult;
    try {
      const jsonMatch = content.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        analysisResult = JSON.parse(jsonMatch[0]);
      } else {
        analysisResult = JSON.parse(content);
      }
    } catch (parseError) {
      console.error('Failed to parse AI response:', content);
      throw new Error('Invalid AI response format');
    }

    // Get recommendations based on detected disease
    let recommendations: string[] = [];
    if (analysisResult.status === 'diseased' && analysisResult.disease !== 'none') {
      const diseaseInfo = getRecommendations(analysisResult.disease);
      recommendations = diseaseInfo.recommendations;
    } else if (analysisResult.status === 'healthy') {
      recommendations = [
        "Continue regular watering schedule",
        "Maintain proper fertilization routine",
        "Monitor plants regularly for early disease detection",
        "Ensure adequate sunlight exposure",
        "Keep the growing area clean and free of debris"
      ];
    }

    const result = {
      ...analysisResult,
      recommendations,
      timestamp: new Date().toISOString()
    };

    console.log('Analysis complete:', result);

    return new Response(
      JSON.stringify(result),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );

  } catch (error) {
    console.error('Error in analyze-plant function:', error);
    return new Response(
      JSON.stringify({ 
        error: error instanceof Error ? error.message : 'Unknown error occurred',
        details: 'Please ensure you uploaded a valid plant image and try again.'
      }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  }
});
