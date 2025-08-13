# Inbox

- [ ] ! Detect which approval/received files are not used when running the whole test suite. Support automatic removal of those files.
- [ ] Use proper assertionError for better context
- [ ] Support approval directory setting by user
- [ ] Support user config (in contrast to project config). A developer's preferred approver might be different from the next developer.
- [ ] Support iOS
- [ ] Make detailed comparison w/ code between this plugin and Syrupy and Apporvaltesting.
- [ ] Add binary flag to reporters to denote if they can open binary.
- [ ] Integrate image compare -> How should user be able to choose compare method?
- [ ] Add geojson verify wich generate a link to geojson.io and shows only the link in diff tool
- [ ] Make image comperator optional (because of dependencies)
- [ ] Use hash in filename for pytest parametrized test only if a certain number of characters are reach or special characters are in use.
- [ ] autoapproval support via cli flag. Useful if one does refactoring in tests (e.g. renaming).


## Done
- [x] Detect if verify is called multiple times in one test function and generate unique names or at least warn the user.
  - [x] Namer should support multiple calls of verify in one test case
