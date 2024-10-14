package xray

// Test Xray Config.
// datDir means the dir which geosite.dat and geoip.dat are in.
// configPath means the config.json file path.
func TestXray(datDir string, config string) error {
	InitEnv(datDir)
	server, err := StartXray(config)
	if err != nil {
		return err
	}
	err = server.Close()
	if err != nil {
		return err
	}
	return nil
}
