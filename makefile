
activate_env:
	conda activate rekord_master

build_swift_calibrator:
	swift build --package-path Sources

create_binary_sym_link:
	ln -s .build/arm64-apple-macosx/debug/swift-calibrator ./swift-calibrator