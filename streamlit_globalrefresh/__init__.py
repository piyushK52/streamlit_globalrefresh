import os
import time
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "st_globalrefresh",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_globalrefresh", path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def st_globalrefresh(
    action,
    lock_state=False,
    lock_expiration=30000,
    interval=1000,
    *,
    limit=None,
    key=None,
):
    """Create an widget instance to trigger a refresh of the application

    Parameters
    ----------
    interval: int
        Amount of time in milliseconds to regularly refresh the app
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

    Returns
    -------
    int
        Number of times the refresh has been triggered or max value of int
    """

    res = _component_func(
        action=action,
        lock_state=lock_state,
        lock_expiration=lock_expiration,
        interval=interval,
        limit=limit,
        key=key,
    )

    return res


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/__init__.py`
if not _RELEASE:
    import streamlit as st

    st.info(
        """
        Set the interval greater than or equal to 5 secs and less than the lock_expiration time
        which defaults to 30 secs.        
    """
    )

    st.button("Click me for a distraction")

    # We use the special "key" argument to assign a fixed identity to this
    # component instance. By default, when a component's arguments change,
    # it is considered a new instance and will be re-mounted on the frontend
    # and lose its current state. In this case, we want to vary the component's
    # "name" argument without having it get recreated.
    # Run the autorefresh about every 2000 milliseconds (2 seconds) and stop
    # after it's been refreshed 100 times.

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
