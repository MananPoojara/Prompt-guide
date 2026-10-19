# The capstone now continues through a reviewed update

The [second capstone stage](../labs/capstone-update/README.md) integrates lookup, a controlled read failure, checkpoint continuation in a new process, an evidence-linked proposal, and a separate scripted approval/apply gate. Four actual model calls are retained. The first process pauses after the failure; the resumed process keeps the same budget and history.

The host resolves an exact source quotation to offsets, addressing an interface weakness exposed in the read-only stage. This is one new task, not a controlled comparison proving that quotation-based output is more accurate. The [results](../labs/capstone-update/RESULTS.md) show the exact proposal, source, checkpoint, and disposition.

The reviewer remains a scripted fixture. Unapproved, tampered, and stale-target applies are rejected in a disposable directory; the exact reviewed proposal applies and same-process replay returns already_applied. These authored probes are separate from model behavior and do not establish human approval or distributed exactly-once execution.

Fourteen tests and an offline trace checker accompany the lab. The repository gate now includes 23 saved-evidence checks. Both capstone stages are implemented as teaching demonstrations; independent human feedback, annotations, judge calibration, and recurring editorial continuity remain open.
