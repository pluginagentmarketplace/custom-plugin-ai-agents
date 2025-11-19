#!/bin/bash
# Generate personalized learning recommendations after assessment

TECHNOLOGY=$1
SCORE=$2
LEVEL=$3

echo "=== Personalized Learning Recommendations ==="
echo "Technology: $TECHNOLOGY"
echo "Your Score: $SCORE%"
echo "Current Level: $LEVEL"
echo ""

if [ "$SCORE" -lt 50 ]; then
  echo "📚 Recommended Action: Review Fundamentals"
  echo "   - Revisit /roadmap $TECHNOLOGY beginner"
  echo "   - Complete 2-3 beginner projects"
  echo "   - Study time: 2-4 weeks"
elif [ "$SCORE" -lt 70 ]; then
  echo "📈 Recommended Action: Practice More"
  echo "   - Build /project $TECHNOLOGY intermediate"
  echo "   - Review weak areas identified in assessment"
  echo "   - Study time: 4-6 weeks"
elif [ "$SCORE" -lt 85 ]; then
  echo "🚀 Recommended Action: Advance Your Skills"
  echo "   - Tackle /project $TECHNOLOGY advanced"
  echo "   - Explore advanced topics in /roadmap $TECHNOLOGY"
  echo "   - Study time: 6-8 weeks"
else
  echo "🌟 Excellent! Next Steps:"
  echo "   - Consider teaching others (write blog posts)"
  echo "   - Contribute to open source projects"
  echo "   - Explore related technologies"
  echo "   - Take /assess $TECHNOLOGY expert for advanced challenges"
fi

echo ""
echo "Use /resources $TECHNOLOGY to find learning materials!"
