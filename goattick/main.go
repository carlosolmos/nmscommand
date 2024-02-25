package main

import (
	"fmt"
	"nmscommand/model"
	"nmscommand/tui"
	"os"

	tea "github.com/charmbracelet/bubbletea"
)

var (
	//nmscommandVersion = "0.0.1"
	missionRepository model.MissionRepository
)

func main() {

	db := model.InitDB(model.DBFile)
	missionRepository = model.NewMissionRepository(db)

	p := tea.NewProgram(tui.InitialTUIModel(missionRepository))
	if _, err := p.Run(); err != nil {
		fmt.Printf("There's been an error: %v", err)
		os.Exit(1)
	}
}
