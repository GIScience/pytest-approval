# Inbox

- [ ] ! Detect which approval/received files are not used when running the whole test suite. Support automatic removal of those files.
- [ ] Run in auto-approve mode. 
  - This could be a solution for previous task as well. Remove all cassettes and run in auto-approve mode
  - Implement via cli flag. 
  - Useful if one does refactoring in tests (e.g. renaming).
- [ ] Support approval directory setting by user
- [ ] Support user config (in contrast to project config). A developer's preferred approver might be different from the next developer.
- [ ] Support MacOS
- [ ] Make detailed comparison w/ code between this plugin and Syrupy and Apporvaltesting.
- [ ] Add binary flag to reporters to denote if they can open binary
  - User preferred reporter might differ depending of file type.
- [ ] Add geojson verify wich generate a link to geojson.io and shows only the link in diff tool
- [ ] Use hash in filename for pytest parametrized test only if a certain number of characters are reach or special characters are in use
- [ ] Support scrubbing of sensitive or always changing data (like timestamp) data
  - might not be necessary to support, since this can always be done by the user before passing data to verify


## Done
- [x] Detect if verify is called multiple times in one test function and generate unique names or at least warn the user.
  - [x] Namer should support multiple calls of verify in one test case
- [x] Make image comperator optional (because of dependencies)
