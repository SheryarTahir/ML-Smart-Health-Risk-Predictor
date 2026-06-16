# Viva — Questions & Answers

**Q1. Why three algorithms?**
Random Forest, Logistic Regression and SVM cover three different learning
paradigms (bagging tree ensemble, linear probabilistic, max-margin kernel)
so we can pick the one that best fits each dataset rather than assuming a
single model wins everywhere.

**Q2. How do you avoid data leakage?**
We split before scaling, fit the `StandardScaler` only on training data,
then transform the test set with the same scaler. The scaler is saved
alongside the model so inference uses the exact same transformation.

**Q3. How is the best model chosen?**
By hold-out accuracy on the stratified 20% test set; 5-fold CV is reported
for stability.

**Q4. Why JWT instead of Flask sessions?**
JWT is stateless and works equally well for the web frontend and the
Flutter mobile app — no shared cookie domain required.

**Q5. How are passwords stored?**
With `bcrypt`. We never store the plaintext password; only the salted hash.

**Q6. Why MongoDB?**
Predictions have variable schemas (different features per disease) — a
document store fits naturally. Atlas provides a free managed tier.

**Q7. How would you scale this?**
Horizontal: stateless Flask behind a load balancer; MongoDB Atlas
auto-scale tier. ML inference is CPU-bound and milliseconds per request —
add a Redis cache for repeated identical inputs if needed.

**Q8. How would you add explainability?**
Integrate SHAP — compute per-feature contributions at prediction time and
return them in the JSON, then render a horizontal bar in the dashboard.

**Q9. What are the limitations?**
The datasets are small and US-centric; results may not transfer to other
populations. Predictions are NOT medical advice — the UI reinforces this.

**Q10. How is CORS handled?**
`flask-cors` is registered on the app with `*` for development; in
production restrict it to the deployed frontend URL.
