# Privacy-Safe Account Migration Checklist

This repository branch is prepared as a working-tree source for migration to a separate account.

## Required migration method

**Do not transfer or mirror the original Git repository if account separation matters.**

Use a snapshot of the files from this branch, remove all Git metadata, then create a new repository and a new Git history under the destination account.

Recommended sequence:

1. Download/export this branch as a file snapshot.
2. Verify that the exported folder does **not** contain a `.git/` directory.
3. Search the exported files for:
   - personal GitHub usernames;
   - personal email addresses;
   - profile/avatar URLs;
   - account-owned private repository paths;
   - `/Users/...`, `/home/...`, or `C:\Users\...` absolute paths;
   - API keys, tokens, passwords, private keys, cookies, recovery codes, or credentials;
   - `.env` files and local editor/config files.
4. Create a new **private** repository in the destination account.
5. Initialize a fresh Git history from the exported files.
6. Use the destination account's author identity for the first commit.
7. Push only the fresh history to the destination repository.
8. Re-run the privacy search on the destination repository.
9. Only after the destination copy is verified should the source repository be deleted.

## Repository-specific audit status

The migration branch has been checked for obvious account-specific markers in the repository configuration and automation layer. The existing GitHub Actions workflows use the standard `github-actions[bot]` commit identity, and the monitoring configuration contains public data-source settings rather than personal credentials.

No `.env`, credential-, token-, secret-, or key-named repository paths were found in the migration-branch tree during preparation. This is a practical audit, not a guarantee that every historical Git object is free of sensitive information; that is why the destination repository must use a fresh history.

## GitHub Actions after migration

The workflow files can be copied as ordinary repository content, but GitHub platform secrets and permissions are account/repository settings and are not contained in this snapshot.

After migration:

1. Review Actions permissions in the destination repository.
2. Recreate only the secrets actually required by future workflows.
3. Prefer newly generated destination-account credentials rather than copying old credentials.
4. Trigger each workflow manually once and verify that automated commits use only the bot identity.

## What a fresh history prevents from carrying over

A fresh repository history avoids copying historical commit author metadata, old branches and tags, deleted historical blobs, old remote URLs, and other Git ancestry that can directly link the destination repository to the source account.

## What must be recreated separately

Recreate only what is needed in the destination account, including repository visibility, Actions permissions, branch rules, collaborators, webhooks, deployment keys, and repository/environment secrets.
