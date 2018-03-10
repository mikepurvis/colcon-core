# Copyright 2016-2018 Dirk Thomas
# Licensed under the Apache License, Version 2.0

import sys
import time

from colcon_core.event.job import JobEnded
from colcon_core.event.job import JobStarted
from colcon_core.event_handler import EventHandlerExtensionPoint
from colcon_core.plugin_system import satisfies_version
from colcon_core.subprocess import SIGINT_RESULT


class ConsoleStartEndEventHandler(EventHandlerExtensionPoint):
    """
    Output task name on start/end.

    The extension handles events of the following types:
    - :py:class:`colcon_core.event.job.JobStarted`
    - :py:class:`colcon_core.event.job.JobEnded`
    """

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(
            EventHandlerExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')
        self._start_times = {}

    def __call__(self, event):  # noqa: D102
        data = event[0]

        if isinstance(data, JobStarted):
            print(
                'Starting >>> {data.identifier}'.format_map(locals()),
                flush=True)
            self._start_times[data.identifier] = time.time()

        elif isinstance(data, JobEnded):
            duration = time.time() - self._start_times[data.identifier]

            if not data.rc:
                msg = 'Finished <<< {data.identifier} [{duration:.2f}s]' \
                    .format_map(locals())
                writable = sys.stdout

            elif data.rc == SIGINT_RESULT:
                msg = 'Aborted  <<< {data.identifier}'.format_map(locals())
                writable = sys.stdout

            else:
                msg = 'Failed   <<< {data.identifier}\t ' \
                    '[ Exited with code {data.rc} ]'.format_map(locals())
                writable = sys.stderr

            print(msg, file=writable, flush=True)
