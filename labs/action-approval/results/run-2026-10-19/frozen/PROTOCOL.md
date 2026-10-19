# Proposal binding demonstration — 2026-10-19

One gpt-6.1-sol low-reasoning call proposes updating a fictional plan's start time from 13:00 to 14:00 while preserving capacity 20. Supply file contents, original SHA-256, target name, and decision evidence. Retain the exact request/response/log; no retry. A 180-second timeout bounds the call.

The model returns data only and never gets an approval/apply tool. The host first attempts an unapproved apply and records rejection. A scripted review fixture compares the entire proposal to the expected edit before calling the trusted approval method. It then checks that a tampered proposal is rejected, applies the exact approved change inside a fresh temporary directory, and checks same-process replay. Save the final file and event transcript. This is not independent human approval, production authorization, an external deployment, or a crash-safe distributed transaction.

Unit-test path allowlisting, unexpected fields, stale target contents, symlinks, invalid payloads, and exact-proposal binding. The approval state is private to the trusted host process in this example; it is not authenticated or durable. A production review service must establish reviewer authority and isolate that state from the model/runtime. No actual user files or external services are modified by the demonstration.
