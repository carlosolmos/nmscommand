package model

import (
	"database/sql"
	"time"
)

type MissionStage int8

const (
	Planning MissionStage = iota
	Sourcing
	InProgress
	Complete
	Aborted
)

func (ms MissionStage) String() string {
	return [...]string{"Planning", "Sourcing", "In Progress", "Complete", "Aborted"}[ms]
}

type AssetClass int8

const (
	C AssetClass = iota
	B
	A
	S
)

func (ac AssetClass) String() string {
	return [...]string{"C", "B", "A", "S"}[ac]
}

type StarColor int16

const (
	StarYellow StarColor = iota
	StarRed
	StarBlue
	StarGreen
)

func (sc StarColor) String() string {
	return [...]string{"Yellow", "Red", "Blue", "Green"}[sc]
}

func (sc StarColor) Int16() int16 {
	return int16(sc)
}

// Base contains common columns for all tables.
type DBBaseModel struct {
	ID        string `gorm:"type:uuid;primaryKey;default:(gen_random_uuid())"`
	CreatedAt time.Time
	UpdatedAt time.Time
	DeletedAt *time.Time `sql:"index"`
}

type ListItem struct {
	Description string
	Completed   bool
}

type Mission struct {
	DBBaseModel
	Codename    string `gorm:"unique"`
	Description sql.NullString
	StartDate   sql.NullTime
	EndDate     sql.NullTime
	Stage       MissionStage `gorm:"default:0"`
	Milestones  []ListItem   `gorm:"serializer:json"`
	Swag        []ListItem   `gorm:"serializer:json"`
	Tech        []ListItem   `gorm:"serializer:json"`
	Resources   []ListItem   `gorm:"serializer:json"`
	Log         []MissionLogEntry
	Media       []string `gorm:"serializer:json"`
}

type System struct {
	DBBaseModel
	Galaxy       string
	Region       sql.NullString
	System       sql.NullString
	Civilization sql.NullString
	StarColor    sql.NullInt16
	BlackHole    bool
	Atlas        bool
	Outlaw       bool
}

type Planet struct {
	DBBaseModel
	SystemID     string `gorm:"not null"`
	Name         string
	Type         sql.NullString
	Alias        sql.NullString
	PortalCoords []int8   `gorm:"serializer:json"`
	Resources    []string `gorm:"serializer:json"`
	Ecosystem    []string `gorm:"serializer:json"`
	Description  string
	Dissonant    bool
	Media        []string `gorm:"serializer:json"`
}

type MissionLogEntry struct {
	DBBaseModel
	MissionID string `gorm:"not null"`
	Entry     string
	SystemID  sql.NullString
	PlanetID  sql.NullString
	BaseID    sql.NullString
	Media     []string `gorm:"serializer:json"`
}

type Discovery struct {
	DBBaseModel
	SystemID    sql.NullString
	PlanetID    sql.NullString
	Description string
	Wonder      bool
	Media       []string `gorm:"serializer:json"`
}

type Base struct {
	DBBaseModel
	PlanetID    string `gorm:"not null"`
	BaseName    string
	BaseType    sql.NullString
	Description sql.NullString
	Ammenities  []string `gorm:"serializer:json"`
	Resources   []string `gorm:"serializer:json"`
	Media       []string `gorm:"serializer:json"`
}

func NewNullString(s string) sql.NullString {
	return sql.NullString{String: s, Valid: true}
}

func NewNullInt16(i int16) sql.NullInt16 {
	return sql.NullInt16{Int16: i, Valid: true}
}
