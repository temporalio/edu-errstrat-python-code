## Exercise #3: Rollback with the Saga Pattern

During this exercise, you will:

- Orchestrate Activities using a Saga pattern to implement compensating transactions
- Handle failures with rollback logic

Make your changes to the code in the `practice` subdirectory (look for `TODO` 
comments that will guide you to where you should make changes to the code). 
If you need a hint or want to verify your changes, look at the complete version 
in the `solution` subdirectory.

## Setup & Prerequisites

1. In all terminals, change to the `exercises/sagas/practice`
   directory using the following command:
   ```bash
   cd exercises/sagas/practice
   ```
   or, if you're in the GitPod environment:
   ```bash
   ex3
   ```

## Part A: Review your new rollback Activities and custom Error

This Exercise uses the same structure as in the previous Exercises — meaning 
that it will fail at the very end on `ProcessCreditCard` if you provide it with 
a bad credit card number.

Three new Activities have been created to demonstrate rollback actions.

* `update_inventory` is a new step that would run normally (whether or not the
Workflow encounters an error). 
* `revert_inventory` has also been added as a compensating action for `update_inventory`. 
* `refund_customer` has been added as a compensating action for `send_bill`.

Lastly, A custom error, `TestError`, has been implemented in `shared.py` for you to 
use to raise in various places to simulate an error.


1. Review these new Activities at the end of the `activities.py` file. None of
   them make actual inventory or billing changes, because the intent of this
   Activity is to show Temporal features, but you should be able to see where
   you could add functionality here.
2. Review the `TestError` in `shared.py`. This is a error you'll use to simulate
   failure within your Workflow. Similarly to the other errors, it is minimal, but
   hopefully provides an example to follow for creating your own custom errors.
3. Close the file.

## Part B: Add your new rollback Activities to your Workflow

Now you will implement a compensating action using Activities in your Temporal
Workflow.

1. Open `workflow.py`. 
2. Note that a list, `compensations`, has been added at the top to keep track of
   each Activities compensating action. 
3. The `update_inventory` Activity invocation has been added to your Workflow after 
   validating an order, before the `send_bill` Activity is called. The compensating
   action was added to the `compensations` list in the line above. Study this
   and use it for the next step.
4. Locate the invocation for the `process_credit_card` method. Add the appropriate
   dict to the `compensations` list, containing the compensating Activity and
   input. Use the previous step as a reference.  


## Part C: Test the Rollback of Your Activities

Now that you've implemented the Saga pattern, it's time to see it in action. You'll
first execute the Workflow successfully, then introduce an error causing a 
rollback. 

1. In one terminal, start the Worker by running:
   ```bash
   python worker.py
   ```
   or, if you're in the GitPod environment, run:
   ```bash
   ex3w
   ```
2. In another terminal, start the Workflow by executing:
   ```bash
   python starter.py
   ```
   or, if you're in the GitPod environment, run:
   ```bash
   ex3st
   ```
3. The Workflow should complete successfully. Verify its status is **Completed** in
   the Web UI. 
4. Kill the worker using `^C`
5. Open `activities.py`
6. Uncomment the following line in the `process_credit_card` Activity
   ```python
   raise ApplicationError(
      "Test Error. Rolling back previous Activities.",
      TestError.__name__,
      non_retryable=True,
   )
   ```
7. Restart the Worker by running:
   ```bash
   python worker.py
   ```
   or, if you're in the GitPod environment, run:
   ```bash
   ex3w
   ```
8. In another terminal, start the Workflow again by executing:
   ```bash
   python starter.py
   ```
   or, if you're in the GitPod environment, run:
   ```bash
   ex3st
   ```
9. You should see the following line within the Stack Trace in the Terminal where
   your Worker was running.
   ```bash
   ERROR:temporalio.workflow:. Rolling back previous Activities.
   ```
10. Check the Workflow Execution in the Web UI. The Workflow will still be marked
   **Failed**, as the error that was raised in the Activity is re-thrown after the 
   compensation is complete. Locate the following:
   * Where did the Activity Task fail? What was the error message? 
   * Where did the compensations take place?
      * Hint: Look for `Customer Refunded` and `Reverted changes to inventory`.

You have now implemented the Saga pattern using Temporal.

### This is the end of the exercise.
