# Streamlit Globalrefresh

This widget refreshes the entire Streamlit app at regular intervals as provided by the user. This also has locks to stop refresh 
when executing longer pieces of code.

Input parameter details

```
interval: int
    Amount of time in milliseconds to
action: str
    choices - 'start_refresh' , 'set_lock'. start_refresh starts the refresh
    loop (it is advised to be only used once). set_lock activates/deactivates
    the a lock
lock_state: Boolean
    To be passed along when using action = 'set_lock' to activate/deactivate
    the lock
lock_expiration: int
    Time in milliseconds till which an active lock will be valid. Defaults to 30000 ms
limit: int or None
    Amount of refreshes to allow. If none, it will refresh infinitely.
    While infinite refreshes sounds nice, it will continue to utilize
    computing resources.
key: str or None
    An optional key that uniquely identifies this component. If this is
    None, and the component's arguments are changed, the component will
    be re-mounted in the Streamlit frontend and lose its current state.
```

## Sample Code

** NOTE: ** Use interval value greater than or equal to 5 seconds and less than the lock_expiration (defaults to 30 secs)

```
result = st_globalrefresh(action="start_refresh", interval=5 * 1000, key="comp12")
if result and result.get("action") == "update":
    count = result.get("count", 0)

    if count % 2 != 0:
        st.write("running")
        time.sleep(2)
    else:
        n = 10
        st.write(f"waiting {n} seconds")

        st_globalrefresh(action="set_lock", lock_state=True)
        for i in range(n):
            st.write(i)
            time.sleep(1)
        st_globalrefresh(action="set_lock", lock_state=False)
st.write(result)
```

Some parts of this code has been adapted from [Streamlit Autorefresh](https://github.com/kmcgrady/streamlit-autorefresh)
