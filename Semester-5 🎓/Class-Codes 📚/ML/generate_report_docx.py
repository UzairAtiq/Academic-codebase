import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

doc = docx.Document()

# set 1 inch standard margins
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

def add_p(text, space_after=4, bold=False, italic=False, font_size=10.5):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(font_size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(35, 35, 35)
    return p

def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(13)
    run.bold = True
    run.font.color.rgb = RGBColor(15, 60, 120)
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(11.5)
    run.bold = True
    run.font.color.rgb = RGBColor(40, 40, 40)
    return p

def add_image_with_caption(img_path, caption_text, width_inches=5.6):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.keep_with_next = True
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_inches))

        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(8)
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_cap = p_cap.add_run(caption_text)
        run_cap.font.name = 'Calibri'
        run_cap.font.size = Pt(9.0)
        run_cap.italic = True
        run_cap.font.color.rgb = RGBColor(90, 90, 90)

def set_cell_background(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def format_table(table):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(table.rows):
        for cell in row.cells:
            cell.paragraphs[0].paragraph_format.space_after = Pt(2)
            cell.paragraphs[0].paragraph_format.space_before = Pt(2)
            cell.paragraphs[0].paragraph_format.line_spacing = 1.05
            for run in cell.paragraphs[0].runs:
                run.font.name = 'Calibri'
                run.font.size = Pt(9.5)
            if i == 0:
                set_cell_background(cell, "EBF2FA")
                for run in cell.paragraphs[0].runs:
                    run.bold = True
                    run.font.color.rgb = RGBColor(15, 60, 120)

# Title Block
title_p = doc.add_paragraph()
title_p.paragraph_format.space_after = Pt(2)
t_run = title_p.add_run("Winter Wheat Yield Analysis Report")
t_run.font.name = 'Calibri'
t_run.font.size = Pt(18)
t_run.bold = True
t_run.font.color.rgb = RGBColor(15, 60, 120)

sub_p = doc.add_paragraph()
sub_p.paragraph_format.space_after = Pt(12)
s_run = sub_p.add_run("Machine Learning Assignment 1 — Practical Case Study on the UK CYCleSS Dataset")
s_run.font.name = 'Calibri'
s_run.font.size = Pt(11)
s_run.italic = True
s_run.font.color.rgb = RGBColor(80, 80, 80)

# Section 1: Overview
add_heading_1("1. Overview of the Problem and Data")
add_p("The goal of this assignment is to predict how much winter wheat real farms produce across England using a combination of satellite radar measurements, daily weather recordings, and local soil characteristics. We use the open CYCleSS dataset, which tracks precision harvester yields measured in tonnes per hectare (t/ha) between 2015 and 2017.")
add_p("Following the assignment setup, we use 2015 and 2016 to train our models, and we save 2017 as an untouched test set. This temporal split tests whether a model trained on previous seasons can actually predict what will happen in a future growing season.")

# Section 2: Data Cleaning and Verification
add_heading_1("2. Preparing and Verifying the Dataset")
add_heading_2("Record Counts per Year")
add_p("When filtering for winter wheat fields during the spring-summer growing window (March 1 to July 31), we obtained:")
add_p("• 2015: 98 fields (exact match with the reference paper)\n"
      "• 2016: 157 fields (paper lists 158; difference of -1)\n"
      "• 2017: 215 fields (paper lists 216; difference of -1)\n"
      "• Total records: 470 field-year observations.")
add_p("The tiny difference of one record in 2016 and 2017 is because the final public dataset removed noisy yield readings that failed quality checks or fell outside confirmed field boundaries.")

add_heading_2("Missing Data and How It Was Handled")
add_p("The soil data and weather recordings had zero missing numbers. However, satellite radar had 61 fields where certain passes were missing due to satellite flight paths and cloud or signal masking (9 fields in 2015, 17 in 2016, and 35 in 2017). To fix this without peeking ahead, we filled missing values with the median numbers from the 2015–2016 training set.")

add_heading_2("Matching and Multi-Year Field Observations")
add_p("All wheat records matched their respective soil and weather files cleanly on field ID and 10 km grid ID, with zero dropped rows. Looking across years, we found that 11 fields grew wheat in both 2015 and 2016, 15 fields in 2016 and 2017, and 28 fields in 2015 and 2017. This happens naturally because UK farmers rotate their fields between wheat, barley, and oilseed rape every two to three years.")

add_heading_2("Column Date Names")
add_p("The date columns are labeled as year, month, and day (for example, March 23 is written as X2015.03.23, and July 31 is X2015.07.31). There are exactly 153 days between March 1 and July 31.")

# Section 3: Simple Linear Regression
add_heading_1("3. Simple Regression: Rain vs. Wheat Yield")
add_p("We first tested whether seasonal rainfall alone can predict wheat yield using a single-variable linear model. We built this both manually using matrix math and using standard software tools.")

t1 = doc.add_table(rows=5, cols=4)
headers = ["Metric / Parameter", "Hand Math", "Software Tool", "Difference"]
for col_idx, h in enumerate(headers):
    t1.rows[0].cells[col_idx].paragraphs[0].text = h

data_q1 = [
    ["Baseline Intercept", "14.35 t/ha", "14.35 t/ha", "0.000"],
    ["Rainfall Slope", "-0.0162 t/ha per mm", "-0.0162 t/ha per mm", "0.000"],
    ["Training R-squared (2015-16)", "0.1556", "0.1556", "0.000"],
    ["Test R-squared (2017)", "-0.0895", "-0.0895", "0.000"]
]
for row_idx, row_data in enumerate(data_q1):
    for col_idx, val in enumerate(row_data):
        t1.rows[row_idx + 1].cells[col_idx].paragraphs[0].text = val
format_table(t1)

add_heading_2("What This Result Tells Us")
add_p("The manual calculation and software output gave the exact same numbers down to the twelfth decimal place. The negative slope shows that for every 100 mm of extra summer rain, yield dropped by about 1.6 tonnes per hectare during the training years. In England, overly wet summers bring fungal crop diseases, block sunlight, and make the soil too soggy for roots.")
add_p("However, rain alone only explains 15.6% of the variation in the training years, and it completely failed on the 2017 test year with a negative R-squared (-0.0895). This proves that you cannot predict crop yield with rain alone. Real crops depend on a balance of temperature, sunshine, and soil moisture holding capacity.")

# Add Figure 1
add_image_with_caption("assets/fig1_simple_regression.png", 
                       "Figure 1: Simple linear regression line of wheat yield versus seasonal precipitation for training (blue) and testing (orange) observations.")

# Section 4: Soil Collinearity
add_heading_1("4. Soil Texture Problem and How We Fixed It")
add_p("In the soil dataset, clay, silt, and sand add up to roughly 100% for every single field (average 100.00%). This creates a major problem called perfect multicollinearity.")
add_p("Because sand is simply 100 minus clay and silt, one column is completely redundant. When we kept all three in the regression, the mathematical equations tried to divide by numbers near zero. The variance inflation factor (which measures how unstable a feature is) shot up past 18 million for sand, 13 million for silt, and 2 million for clay. The coefficients became wild and meaningless.")
add_p("To fix this, we removed sand from the model, leaving clay and silt to represent the soil texture. After removing sand, the variance inflation factor of clay dropped to 11.4 and silt dropped to 5.1. This made all the numbers stable and reliable.")

# Section 5: Multiple Linear Regression
add_heading_1("5. Multiple Linear Regression and Feature Insights")
add_p("We standardized all features so they have a mean of 0 and a standard deviation of 1. This lets us compare their coefficients fairly.")

add_heading_2("Interpreting Three Key Features")
add_p("1. Sunshine and Solar Radiation (-1.33 t/ha per standard deviation): Strong summer sunshine had a noticeable negative link with wheat yield. In rainfed English fields, intense summer sun usually means dry heatwaves during June and July, drying out the soil right when wheat heads need moisture to fill with grain.")
add_p("2. Total Rainfall (-0.80 t/ha per standard deviation): Even when controlling for sun and soil, extra summer rain was associated with lower yield due to foliar diseases like Septoria leaf blotch and nutrient leaching.")
add_p("3. Soil Clay Percentage (-0.30 t/ha per standard deviation): Heavy clay soils hold water too tightly and can cause springtime waterlogging, which stunts early root growth compared to balanced loamy soils.")

add_heading_2("Why These Are Associations, Not Direct Causes")
add_p("These numbers show correlations in field data, not medical-grade proof of cause and effect. A regression coefficient can pick up things we did not measure, such as how much fertilizer farmers applied, what wheat seed variety they bought, or when they sprayed fungicide. Changing sunshine alone on a real farm without changing heat and evaporation is physically impossible.")

add_heading_2("Predicting a Typical Field")
add_p("If we take a typical English field where every soil and weather feature is set to its exact median value, our multiple regression model predicts a yield of 10.15 tonnes per hectare. This is very close to the actual average yield of 10.23 t/ha.")

# Section 6: Feature Group Ablation
add_heading_1("6. Comparing Different Feature Groups")
add_p("To see what kinds of data actually help predict yield on unseen future years, we tested models trained with only specific groups of features:")

t2 = doc.add_table(rows=5, cols=4)
h2 = ["Feature Group", "Number of Inputs", "Test Error (RMSE)", "Test R-squared"]
for col_idx, h in enumerate(h2):
    t2.rows[0].cells[col_idx].paragraphs[0].text = h

data_q2 = [
    ["Soil Only", "8 features", "2.60 t/ha", "-0.126"],
    ["Weather Only", "4 features", "4.11 t/ha", "-1.811"],
    ["Satellite Radar (SAR) Only", "3 features", "2.36 t/ha", "+0.072"],
    ["All Combined", "15 features", "5.17 t/ha", "-3.455"]
]
for row_idx, row_data in enumerate(data_q2):
    for col_idx, val in enumerate(row_data):
        t2.rows[row_idx + 1].cells[col_idx].paragraphs[0].text = val
format_table(t2)

add_heading_2("What This Comparison Reveals")
add_p("Satellite radar was the only model that achieved a positive R-squared (+0.072) and the lowest error on the test year. Radar bounces radio waves off the plants, measuring the actual physical volume and moisture of the living crop. This physical measurement worked well in 2017.")
add_p("In contrast, weather features alone performed poorly on the test year (R-squared of -1.811). The weather in 2017 had different patterns than 2015 and 2016, so the linear model made big mistakes. When all features were combined, the weather features dragged down the entire model. This shows that simpler, direct plant measurements often beat complex weather models when predicting future years.")

# Section 7: Advanced Metrics
add_heading_1("7. Testing the Metrics and Baseline Comparison")
add_p("We wrote our own code for mean absolute error (MAE), mean squared error (MSE), root mean squared error (RMSE), and R-squared. Every single manual calculation matched the software library outputs with zero error.")
add_p("Comparing with a simple baseline: If we do not use any machine learning at all and simply guess the training average yield (10.15 t/ha) for every field in 2017, we get an error of 2.28 t/ha. This simple baseline actually beat the full weather-heavy linear regression model on the test year because the linear weather coefficients had overfit to the earlier seasons.")

# Section 8: Outliers and Sensitivity
add_heading_1("8. Large Errors and Outlier Analysis")
add_p("Squared error metrics like MSE and RMSE penalize large mistakes much more heavily than MAE. For instance, if a prediction is off by 10 t/ha, its squared error is 100, which is 100 times larger than an error of 1 t/ha.")
add_p("When looking at the five fields with the worst predictions, the errors were between 14 and 18 tonnes per hectare. In farm research, these extreme errors usually happen because:")
add_p("• The combine harvester yield sensor lost calibration while moving across large hilly fields.\n"
      "• Localized hail storms or strong summer winds knocked down the stalks (crop lodging).\n"
      "• Severe local fungal blight attacked the roots in a way that regional 10 km weather data could never see.")

# Section 9: Prediction Intervals
add_heading_1("9. 90% Prediction Intervals")
add_p("We built an uncertainty band of roughly plus or minus 2.68 tonnes per hectare around each prediction (a total interval width of 5.37 t/ha), based on how far off the model was on training data.")
add_p("When we tested this on the 2017 harvest, about 64.6% of the real yields fell inside the band instead of the planned 90%. The intervals were too narrow because 2017 had a weather shift that the training data did not anticipate, and real agricultural errors have fatter tails than a textbook bell curve.")

# Add Figure 2
add_image_with_caption("assets/fig2_prediction_intervals.png", 
                       "Figure 2: Approximate 90% prediction intervals for 2017 test fields, displaying predicted yields with uncertainty margins alongside actual harvest yields.")

# Section 10: Gradient Descent
add_heading_1("10. Gradient Descent Step by Step")
add_heading_2("Finding the Gradient Formula")
add_p("The mean squared error measures the average squared difference between predictions and actual yields. Taking the derivative with respect to the weights gives a simple rule: the gradient equals the average of the prediction error multiplied by each feature. This tells the algorithm which direction to adjust each weight.")

add_heading_2("Running the Algorithm")
add_p("Starting with all weights set to zero and a learning rate of 0.1:")
add_p("• Step 1: Loss was 53.41.\n"
      "• Step 10: Loss dropped quickly down to 9.20.\n"
      "• Convergence: The algorithm settled smoothly at a loss of 1.32, matching the exact direct formula parameters with a maximum difference of less than 0.05.")

# Add Figure 3
add_image_with_caption("assets/fig3_cost_and_params.png", 
                       "Figure 3: Cost function reduction during gradient descent (left) and comparison of final learned parameters against the exact direct formula (right).", width_inches=6.0)

add_heading_2("Testing Learning Rates")
add_p("• Learning rates between 0.01 and 0.5 converged smoothly.\n"
      "• At 1.0, steps were fast and reached the edge of stability.\n"
      "• At 1.2 and higher, the steps jumped over the lowest point, causing the loss to explode toward infinity.")

# Add Figure 4
add_image_with_caption("assets/fig4_learning_rates.png", 
                       "Figure 4: Gradient descent cost trajectories across different learning rates, illustrating stable convergence versus divergence at large step sizes.")

add_heading_2("Why Feature Scaling Is Essential")
add_p("When we tried running gradient descent on unscaled, raw numbers (where radar is around -1200, rainfall is around 260, and water capacity is 0.1), the calculations failed on the very first step. Because gradient steps depend on feature sizes, large features took gigantic jumps while small features barely moved. Scaling every feature to the same size creates a balanced bowl shape where gradient descent moves straight toward the minimum.")

# Section 11: Normal Equation vs Gradient Descent
add_heading_1("11. Normal Equation vs. Gradient Descent")
add_heading_2("When to Use Each")
add_p("• Gradient Descent is better when you have tens of thousands of features, or when data is too big to fit into memory and must be processed in small streaming batches.\n"
      "• The Normal Equation is better when you have a small to moderate number of features (under 10,000), because it gives the exact answer in one calculation with zero hyperparameter tuning.")

add_heading_2("Timing Experiment")
add_p("We timed both methods as the number of features grew from 50 to 3,000. The direct normal equation time curved upward steeply like a cube ($O(n^3)$) because inverting big matrices is very heavy. Meanwhile, gradient descent scaled in a gentle straight line ($O(n)$).")

# Add Figure 5
add_image_with_caption("assets/fig5_runtime_scaling.png", 
                       "Figure 5: Runtime benchmark showing cubic growth for the direct normal equation matrix inversion versus linear scaling for gradient descent as feature dimension grows.")

add_heading_2("What Happens When Features Outnumber Data Rows")
add_p("If we used every single daily weather reading and satellite date as an individual feature, we would have thousands of columns for only a few hundred fields ($n > m$). In this case, the matrix becomes singular and cannot be inverted at all. To solve this, we can either add a ridge penalty (L2 regularization) or combine daily numbers into seasonal averages.")

# Section 12: Bonus Tasks
add_heading_1("12. Bonus Tasks")
add_heading_2("Early Stopping")
add_p("We modified gradient descent to stop automatically when the loss changed by less than 0.0001 between steps. It reached this threshold and stopped cleanly in 398 iterations.")

add_heading_2("Random vs. Grouped Cross-Validation")
add_p("We compared standard random 5-fold cross-validation with grouped cross-validation based on 10 km grid squares:")
add_p("• Random 5-Fold Cross-Validation: Error was 1.85 t/ha.\n"
      "• Grouped Cross-Validation by Grid: Error was 2.06 t/ha.\n"
      "• Difference: The random split was 0.21 t/ha (about 10%) too optimistic.")
add_p("Why this happens: In a random split, fields from the exact same neighborhood end up in both training and testing folds. The model 'cheats' by learning the local weather from the training fields and using it on test fields next door. Grouping holds out whole geographic squares at once, giving an honest test of how well the model works in a new area.")

# Section 13: Summary Conclusions
add_heading_1("13. Conclusion")
add_p("1. Simple models often beat overfit complex models when predicting future years with shifting weather.\n"
      "2. Physical satellite radar data transferred to the new year much better than raw weather numbers.\n"
      "3. Always check for collinear features (like soil texture adding to 100%) and scale your inputs before running gradient descent.\n"
      "4. Standard random cross-validation gives overly optimistic numbers on spatial farm data; grouping by geographic area provides a true evaluation.")

target_path = "/Users/uzair/academic-codebase📘/Semester-5 🎓/Class-Codes 📚/ML/ML_Assignment_1_Analysis_Report.docx"
doc.save(target_path)
print(f"Report with pictures successfully saved to: {target_path}")
