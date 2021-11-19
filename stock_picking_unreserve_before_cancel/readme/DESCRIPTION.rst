This module does the following:

- Overrides the action_cancel() method to process unreserve before cancel to clear the
  pack operation records.

The pack operation records will otherwise persist even when the cancelled picking
revives with another operation type (i.e. location_id of the move is changed).
