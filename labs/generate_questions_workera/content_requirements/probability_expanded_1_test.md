# Machine Learning Exam Revision

## 1. Probability & Statistics

### 1.1 Metrics and Model Diagnostics

#### 1.1.1 Confusion Matrix
- **Definition**: A table that describes the performance of a classification model on a set of test data.
- **Key Components**:
  - **True Positives (TP)**: Correctly predicted positive class.
  - **False Positives (FP)**: Incorrectly predicted positive class (Type I error).
  - **True Negatives (TN)**: Correctly predicted negative class.
  - **False Negatives (FN)**: Incorrectly predicted negative class (Type II error).
- **Common Metrics**:
  - **Accuracy**: \( \frac{TP + TN}{TP + FP + TN + FN} \)
  - **Precision**: \( \frac{TP}{TP + FP} \)
  - **Recall (Sensitivity)**: \( \frac{TP}{TP + FN} \)
  - **F1 Score**: Harmonic mean of precision and recall.

#### 1.1.2 Residuals
- **Definition**: The difference between observed and predicted values in regression.
- **Key Concepts**:
  - **Residuals Plot**: A graph to detect patterns that indicate model inadequacy.
  - **Homoscedasticity**: Residuals have constant variance (ideal scenario).
  - **Heteroscedasticity**: Residuals have non-constant variance (indicates model problems).

#### 1.1.3 Effect Sizes
- **Cohen’s d**: Measures the size of the difference between two means.
- **R-Squared (Coefficient of Determination)**: Proportion of variance in the dependent variable explained by the independent variables in the model.
- **ROC Curve**: Plot showing the true positive rate vs. false positive rate.
  - **AUC (Area Under the Curve)**: Measures overall model performance.

---

### 1.2 Probabilistic Theory

#### 1.2.1 Probabilistic Independence
- **Definition**: Two events are independent if the occurrence of one does not affect the probability of the other.
- **Calculation**: \( P(A \cap B) = P(A) \times P(B) \)

#### 1.2.2 Generative and Discriminative Models
- **Generative Models**: Learn the joint probability \( P(X, Y) \) (e.g., Naive Bayes, Gaussian Mixture Models).
- **Discriminative Models**: Learn the conditional probability \( P(Y | X) \) (e.g., Logistic Regression, SVM).

#### 1.2.3 Conditional Probabilities
- **Bayes' Theorem**: \( P(A|B) = \frac{P(B|A) P(A)}{P(B)} \)
- **Total Probability**: Used to find probabilities of complex events by breaking them down.

#### 1.2.4 Probability Distributions
- **Bernoulli Distribution**: Describes outcomes of a binary event.
- **Uniform Distribution**: All outcomes have equal probability.
- **Poisson Distribution**: Models the number of events occurring within a fixed interval.
- **Binomial Distribution**: Models the number of successes in a fixed number of trials.
- **Normal Distribution**: Bell-shaped curve, important for central limit theorem.

#### 1.2.5 Operations on Probabilities
- **Union of Events**: \( P(A \cup B) = P(A) + P(B) - P(A \cap B) \)
- **Intersection of Events**: \( P(A \cap B) = P(A) \times P(B) \) (if independent).
- **Complement**: \( P(\text{not A}) = 1 - P(A) \)

#### 1.2.6 Probability Density Function (PDF)
- **Mean**: The expected value of a random variable.
- **Variance**: Measure of how much values spread out around the mean.
- **Integral for Probability**: \( P(a \leq X \leq b) = \int_a^b f(x) dx \)

---

### 1.3 Similarities
- Both **Confusion Matrix** and **ROC Curve** are used to evaluate classification models.
- **Probability Distributions** like Bernoulli and Binomial are used for discrete events.
- **Generative and Discriminative Models** both attempt to classify data but with different approaches.

---

### 1.4 Differences
- **Confusion Matrix** provides performance at a specific threshold, while **ROC Curve** shows performance across thresholds.
- **Generative Models** focus on modeling data distribution (joint probability), while **Discriminative Models** focus on boundaries (conditional probability).
- **Residuals** are used in regression analysis, whereas **confusion matrices** apply to classification problems.
