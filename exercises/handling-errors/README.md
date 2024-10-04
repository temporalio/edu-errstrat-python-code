## Exercise #1: Handling Errors

During this exercise, you will:

- raise and handle exceptions in Temporal Workflows and Activities
- Use non-retryable errors to fail an Activity
- Locate the details of a failure in Temporal Workflows and Activities in the Event History

Make your changes to the code in the `practice` subdirectory (look for `TODO`
comments that will guide you to where you should make changes to the code). If
you need a hint or want to verify your changes, look at the complete version in
the `solution` subdirectory.

## Setup

You'll need two terminal windows for this exercise.

1. In all terminals, change to the `exercises/handling-errors/practice`
   directory using the following command:
   ```bash
   cd exercises/handling-errors/practice
   ```
   or, if you're in the GitPod environment:
   ```bash
   ex1
   ```

## Part A: raise a non-retryable `ApplicationError` to fail an Activity

In this part of the exercise, you will raise a non-retryable Application Failure 
(represented in Python as `ApplicationError`) that will fail your Activities.

Application Failures are used to communicate application-specific failures in
Workflows and Activities. In Activities, raising an `ApplicationError` will
cause the Activity to fail. However, this unless this Activity is specified as
non-retryable, it will retry according to the Retry Policy. To have an Activity
fail when an `ApplicationError` is raised, set it as non-retryable. Any other 
exception that is raised in a Python activity is automatically converted to an `ApplicationError`
upon being raised.

1. Open the `shared.py` file and familiarize yourself with the
   dataclasses you will be using during the exercise. Pay particular attention
   to the custom error definitions.
2. Open the `activities.py` file in your text editor.
3. Add the following import statement `from temporalio.exceptions import ApplicationError`
   at the top of this file.
4. In the `send_bill` Activity, notice how an error is raised if the `chargeAmount`
   is less than 0. If the calculated amount to charge the customer is negative,
   a non-retryable `ApplicationError` is raised. It is important to use a
   non-retryable failure here, as you want to fail the Activity if the amount
   was calculated to be negative. In this error, we pass a reason for the failure
   and the type of error that is being converted to an `ApplicationError`.
5. Go to `process_credit_card` Activity, where you will raise an `ApplicationError`
   if the credit card fails its validation step. In this Activity, you will raise
   an error if the entered credit card number does not have 16 digits. Use the
   `ApplicationError` code from the previous step as a reference. You should
   set the type as `CreditCardProcessingError`.
6. Save your file.

## Part B: Catch the `ActivityError`

In this part of the exercise, you will catch the `ApplicationError` that was
raised from the `processCreditCard` Activity and handle it.

1. Open the `workflow.py` in your text editor.
2. Locate the line with that beings with: `credit_card_confirmation = await workflow.execute_activity_method`.
   1. This code calls the `process_credit_card` Activity, and if a non-retryable
      `ApplicationError` is raised, the Workflow will fail. However, it is possible
      to catch this failure and either handle it, or continue to propagate it up.
   2. Wrap this line in a `try/catch` block. However, you will not catch `ApplicationError`.
      Since the `ApplicationError` in the Activity is designated as non-retryable,
      by the time it reaches the Workflow it is converted to an `ActvityError`.
   3. Within the `catch` block, add a logging statement stating that the Activity
      has failed.
   4. After the logging statement, raise another `ApplicationError` passing in a 
      message and setting `CreditCardProcessingError` as the  type. This will cause the
      Workflow to fail, as you were unable to bill the customer.
3. Save your file.

## Part C: Run the Workflow

In this part of the exercise, you will run your Workflow and see both your
Workflow and Activity succeed and fail.

In the `starter.py` file, a valid credit card number as part of an order has
been provided to run this Workflow.

**First, run the Workflow successfully:**

1. In the same terminal, start the Worker by running:
   ```bash
   python worker.py
   ```
   or, if you're in the GitPod environment, run:
   ```bash
   ex1w
   ```
3. In another terminal, start the Workflow by executing `starter.py`:
   ```bash
   python starter.py
   ```
   or, if you're in the GitPod environment, run:
   ```bash
   ex1st
   ```
4. In the Web UI, verify that the Workflow ran successfully to completion.

**Next, you'll modify the starter data to cause the Workflow to fail:**

1. Open `shared.py` and modify the code
   ```python
    credit_card_info = CreditCardInfo(
        holderName="Lisa Anderson", number="424242424242424"
    )
   ```
   by deleting a digit from the String. Save this file.
2. Stop the worker using **CMD-C** on Mac or **Ctrl-C** on Windows/Linux
3. Restart the Worker by running:
   ```bash
   python worker.py
   ```
   or, if you're in the GitPod environment, run:
   ```bash
   ex1w
   ```
5. In another terminal, start the Workflow by executing `starter.py`:
   ```bash
   python starter.py
   ```
   or, if you're in the GitPod environment, run:
   ```bash
   ex1st
   ```
6. You should see the Workflow fail in the terminal where you executed `starter.py`.
   Also check the WebUI and view the failure there.

### This is the end of the exercise.
