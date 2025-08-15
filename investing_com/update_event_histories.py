from important_events import important_events
from event_history_funcs import events_to_update, update_event_histories


if __name__ == "__main__":

    # Dict of all important events
    imp_events = important_events()

    # List event histories to update
    events_today = events_to_update('./csvs/econ_calendar.csv', imp_events)

    # Update event histories
    update = update_event_histories(imp_events, events_today, './csvs/')

    # Update all event histories
    update_all = update_event_histories(imp_events, imp_events.keys(), './csvs/')



